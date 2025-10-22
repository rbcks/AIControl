"""SQLAlchemy models for the assessment workflow.// 평가 워크플로우를 위한 SQLAlchemy 모델."""
from __future__ import annotations

import json
from typing import Dict, List

from sqlalchemy import Boolean, Column, Integer, String, Text

from db import Base


class AssessmentSession(Base):
    """Persisted assessment session.// 지속적으로 저장되는 평가 세션."""

    __tablename__ = "assessment_sessions"

    session_id = Column(String, primary_key=True, index=True)
    traits = Column(Text, default="{}")
    answers = Column(Text, default="{}")
    asked_questions = Column(Text, default="[]")
    current_stage = Column(Integer, default=1)
    completed = Column(Boolean, default=False)
    slug = Column(String, unique=True, nullable=True)

    def get_trait_vector(self) -> Dict[str, float]:
        """Return traits as a dictionary.// traits를 사전 형태로 반환."""
        if self.traits:
            return json.loads(self.traits)
        return {}

    def set_trait_vector(self, traits: Dict[str, float]) -> None:
        """Serialize trait vector.// trait 벡터를 직렬화."""
        self.traits = json.dumps(traits)

    def get_answers(self) -> Dict[str, int]:
        """Return answers map.// 답변 맵 반환."""
        if self.answers:
            return json.loads(self.answers)
        return {}

    def set_answers(self, answers: Dict[str, int]) -> None:
        """Serialize answer map.// 답변 맵 직렬화."""
        self.answers = json.dumps(answers)

    def get_asked_questions(self) -> List[str]:
        """Return list of asked question IDs.// 제시된 문항 ID 목록 반환."""
        if self.asked_questions:
            return json.loads(self.asked_questions)
        return []

    def set_asked_questions(self, question_ids: List[str]) -> None:
        """Serialize asked questions list.// 제시된 문항 목록 직렬화."""
        self.asked_questions = json.dumps(question_ids)
