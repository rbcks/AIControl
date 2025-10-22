"""Scoring utilities.// 점수 계산 유틸리티."""
from __future__ import annotations

from typing import Dict

from engine.state import TraitState, weighted_delta


def apply_answer(state: TraitState, question: Dict, answer_value: int) -> TraitState:
    """Update trait state based on question weights.// 문항 가중치로 trait 상태를 업데이트."""
    weights: Dict[str, float] = question.get("weights", {})
    delta = weighted_delta(weights, answer_value)
    state.update(delta)
    return state
