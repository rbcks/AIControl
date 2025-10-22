"""FastAPI application entry point.// FastAPI 애플리케이션 엔트리 포인트."""
from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import Base, engine, get_session
from engine import recommender, routing, scorer
from engine.state import TraitState
from models import AssessmentSession

APP_DIR = Path(__file__).resolve().parent
ITEM_BANK_DIR = APP_DIR / "item_bank"
QUESTIONS = json.loads((ITEM_BANK_DIR / "questions_v1.json").read_text(encoding="utf-8"))
CAREERS = json.loads((ITEM_BANK_DIR / "career_profiles_v1.json").read_text(encoding="utf-8"))
STAGE_BREAKPOINTS = [3, 6, 9]

app = FastAPI(title="Career Insight API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Question(BaseModel):
    """Public question representation.// 외부에 노출되는 문항 표현."""

    id: str
    text: str
    dimension: str


class StartResponse(BaseModel):
    """Response for start endpoint.// 시작 엔드포인트 응답."""

    session_id: str
    questions: List[Question]


class AnswerRequest(BaseModel):
    """Request payload for answering a question.// 문항 응답 요청 페이로드."""

    session_id: str
    question_id: str
    answer_value: int


class AnswerResponse(BaseModel):
    """Response after processing an answer.// 응답 처리 후 반환."""

    completed: bool
    next_question: Optional[Question]
    progress: Dict[str, int]


class ResultRequest(BaseModel):
    """Request for result computation.// 결과 계산 요청."""

    session_id: str


class Recommendation(BaseModel):
    """Recommended career summary.// 추천 커리어 요약."""

    career: str
    score: float
    description: str
    reasons: List[str]
    growth_plan: List[str]
    bonus: float
    penalty: float


class ResultResponse(BaseModel):
    """Result payload for the client.// 클라이언트용 결과 페이로드."""

    session_id: str
    slug: str
    recommendations: List[Recommendation]


@app.on_event("startup")
def on_startup() -> None:
    """Create database schema.// 데이터베이스 스키마 생성."""
    Base.metadata.create_all(bind=engine)


@app.post("/start", response_model=StartResponse)
def start_assessment(db: Session = Depends(get_session)) -> StartResponse:
    """Create a new assessment session.// 새로운 평가 세션 생성."""
    session_id = str(uuid.uuid4())
    session = AssessmentSession(session_id=session_id)
    session.set_trait_vector(TraitState().to_dict())
    session.set_answers({})
    session.set_asked_questions([])
    db.add(session)

    initial = routing.initial_questions(QUESTIONS)
    session.set_asked_questions([q["id"] for q in initial])
    db.add(session)

    return StartResponse(
        session_id=session_id,
        questions=[Question(id=q["id"], text=q["text"], dimension=q["dimension"]) for q in initial],
    )


def _get_session_or_404(db: Session, session_id: str) -> AssessmentSession:
    session = db.query(AssessmentSession).filter(AssessmentSession.session_id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


def _update_stage(session: AssessmentSession) -> None:
    answered_count = len(session.get_answers())
    stage = 1
    for idx, threshold in enumerate(STAGE_BREAKPOINTS, start=1):
        if answered_count >= threshold:
            stage = idx
    session.current_stage = stage
    session.completed = answered_count >= STAGE_BREAKPOINTS[-1]


@app.post("/answer", response_model=AnswerResponse)
def answer_question(payload: AnswerRequest, db: Session = Depends(get_session)) -> AnswerResponse:
    """Store an answer and return the next question.// 답변을 저장하고 다음 문항 반환."""
    if payload.answer_value < 1 or payload.answer_value > 5:
        raise HTTPException(status_code=400, detail="Answer must be between 1 and 5")

    session = _get_session_or_404(db, payload.session_id)
    answers = session.get_answers()
    answers[payload.question_id] = payload.answer_value
    session.set_answers(answers)

    trait_state = TraitState.from_existing(session.get_trait_vector())
    question = next((q for q in QUESTIONS if q["id"] == payload.question_id), None)
    if not question:
        raise HTTPException(status_code=400, detail="Question not found")
    scorer.apply_answer(trait_state, question, payload.answer_value)
    session.set_trait_vector(trait_state.to_dict())

    asked = session.get_asked_questions()
    if payload.question_id not in asked:
        asked.append(payload.question_id)
    session.set_asked_questions(asked)

    _update_stage(session)

    next_q_raw = routing.next_question(QUESTIONS, asked, answers)
    if next_q_raw:
        asked.append(next_q_raw["id"])
        session.set_asked_questions(asked)
        next_question_model = Question(
            id=next_q_raw["id"], text=next_q_raw["text"], dimension=next_q_raw["dimension"]
        )
    else:
        next_question_model = None

    _update_stage(session)

    progress = {"answered": len(session.get_answers()), "stage": session.current_stage}
    return AnswerResponse(
        completed=session.completed,
        next_question=next_question_model,
        progress=progress,
    )


@app.post("/result", response_model=ResultResponse)
def get_result(payload: ResultRequest, db: Session = Depends(get_session)) -> ResultResponse:
    """Compute and return recommendations.// 추천 결과 계산 및 반환."""
    session = _get_session_or_404(db, payload.session_id)
    trait_state = TraitState.from_existing(session.get_trait_vector())

    recommendations = recommender.recommend_careers(trait_state, CAREERS)
    slug = session.slug
    if not slug:
        slug = uuid.uuid4().hex[:10]
        session.slug = slug

    return ResultResponse(session_id=session.session_id, slug=slug, recommendations=recommendations)
