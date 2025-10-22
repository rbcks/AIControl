"""Career recommendation engine.// 커리어 추천 엔진."""
from __future__ import annotations

import math
from typing import Dict, List, Tuple

from engine.state import TraitState


def cosine_similarity(vec_a: Dict[str, float], vec_b: Dict[str, float]) -> float:
    """Compute cosine similarity.// 코사인 유사도 계산."""
    dot = 0.0
    mag_a = 0.0
    mag_b = 0.0
    for trait in set(vec_a.keys()) | set(vec_b.keys()):
        a = vec_a.get(trait, 0.0)
        b = vec_b.get(trait, 0.0)
        dot += a * b
        mag_a += a * a
        mag_b += b * b
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / math.sqrt(mag_a * mag_b)


def value_bonus(user_values: Dict[str, float], career: Dict) -> float:
    """Positive bonus when value tags align.// 가치 태그가 정렬될 때 보너스."""
    bonus = 0.0
    desired = set(career.get("values", []))
    for value_tag in desired:
        bonus += user_values.get(value_tag, 0.0) * 0.05
    return bonus


def conflict_penalty(user_values: Dict[str, float], career: Dict) -> float:
    """Penalty when user values conflict.// 사용자 가치와 충돌 시 패널티."""
    conflicts = career.get("conflicts", [])
    penalty = 0.0
    for conflict in conflicts:
        penalty += abs(user_values.get(conflict, 0.0)) * 0.07
    return penalty


def recommend_careers(
    trait_state: TraitState,
    career_profiles: List[Dict],
) -> List[Dict]:
    """Return ranked career options.// 순위가 매겨진 커리어 옵션 반환."""
    recommendations: List[Tuple[Dict, float, float, float]] = []
    trait_state.normalize()
    for profile in career_profiles:
        score = cosine_similarity(trait_state.scores, profile.get("traits", {}))
        bonus = value_bonus(trait_state.scores, profile)
        penalty = conflict_penalty(trait_state.scores, profile)
        final_score = score + bonus - penalty
        recommendations.append((profile, final_score, bonus, penalty))

    recommendations.sort(key=lambda item: item[1], reverse=True)
    top = []
    for profile, final_score, bonus, penalty in recommendations[:3]:
        top.append(
            {
                "career": profile["name"],
                "score": round(final_score, 3),
                "description": profile.get("description", ""),
                "reasons": profile.get("fit_notes", []),
                "growth_plan": profile.get("growth_plan", []),
                "bonus": round(bonus, 3),
                "penalty": round(penalty, 3),
            }
        )
    return top
