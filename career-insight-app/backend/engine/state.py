"""Trait state helpers.// 성향 상태 헬퍼."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable


DEFAULT_TRAITS = [
    "creativity",
    "analysis",
    "communication",
    "empathy",
    "structure",
    "exploration",
    "stability",
    "leadership",
]


@dataclass
class TraitState:
    """In-memory representation of trait scores.// Trait 점수의 메모리 표현."""

    scores: Dict[str, float] = field(default_factory=lambda: {trait: 0.0 for trait in DEFAULT_TRAITS})

    def update(self, deltas: Dict[str, float]) -> None:
        """Add deltas to current scores.// 델타 값을 현재 점수에 더함."""
        for trait, value in deltas.items():
            self.scores[trait] = self.scores.get(trait, 0.0) + value

    def normalize(self) -> None:
        """Normalize scores to unit length.// 스코어를 단위 길이로 정규화."""
        magnitude = sum(value ** 2 for value in self.scores.values()) ** 0.5
        if magnitude == 0:
            return
        for trait in list(self.scores.keys()):
            self.scores[trait] /= magnitude

    @classmethod
    def from_existing(cls, data: Dict[str, float]) -> "TraitState":
        """Instantiate from existing data.// 기존 데이터를 기반으로 인스턴스화."""
        state = cls()
        state.scores.update(data)
        return state

    def to_dict(self) -> Dict[str, float]:
        """Return scores as a dict.// 점수를 dict로 반환."""
        return dict(self.scores)


def weighted_delta(weights: Dict[str, float], answer_value: int) -> Dict[str, float]:
    """Calculate trait deltas based on answer.// 답변에 따른 trait 변화량 계산."""
    scale = (answer_value - 3) / 2  # answers 1-5 -> -1 to +1
    return {trait: weight * scale for trait, weight in weights.items()}


def aggregate_traits(trait_vectors: Iterable[Dict[str, float]]) -> Dict[str, float]:
    """Aggregate trait vectors by averaging.// trait 벡터를 평균하여 집계."""
    totals: Dict[str, float] = {trait: 0.0 for trait in DEFAULT_TRAITS}
    counts: Dict[str, int] = {trait: 0 for trait in DEFAULT_TRAITS}
    for vector in trait_vectors:
        for trait, value in vector.items():
            totals[trait] = totals.get(trait, 0.0) + value
            counts[trait] = counts.get(trait, 0) + 1
    return {trait: (totals[trait] / counts[trait]) if counts[trait] else 0.0 for trait in DEFAULT_TRAITS}
