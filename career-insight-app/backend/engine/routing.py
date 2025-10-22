"""Adaptive routing logic for selecting the next question.// 다음 문항을 선택하는 적응형 라우팅 로직."""
from __future__ import annotations

from typing import Dict, List, Optional


def initial_questions(question_bank: List[Dict]) -> List[Dict]:
    """Return the first batch of questions.// 첫 번째 문항 묶음을 반환."""
    return question_bank[:3]


def next_question(
    question_bank: List[Dict],
    asked_ids: List[str],
    answers: Dict[str, int],
) -> Optional[Dict]:
    """Select the next question based on simple branching.// 간단한 분기를 기반으로 다음 문항을 선택."""
    remaining = [q for q in question_bank if q["id"] not in asked_ids]
    if not remaining:
        return None

    # Basic branching example: if user favors creativity, ask project-style question.
    # 기본 분기 예시: 창의성이 높다면 프로젝트 스타일 문항을 추가 제공.
    creativity_score = 0
    if answers:
        creativity_questions = [q for q in question_bank if q.get("focus") == "creativity"]
        for q in creativity_questions:
            value = answers.get(q["id"])
            if value:
                creativity_score += value
    if creativity_score >= 12:
        for q in remaining:
            if q.get("tag") == "project_lead":
                return q

    # Default to next sequential question.// 기본적으로 다음 순차 문항 반환.
    return remaining[0]
