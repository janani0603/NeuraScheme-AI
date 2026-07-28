import logging
from app.agents.profile_agent import AgentState

logger = logging.getLogger(__name__)

TOP_N = 50


def _combined_score(item: dict, completeness: float) -> float:
    e_score = item["eligibility_score"] / 100
    v_score = float(item.get("vector_score", 0.0))
    combined = (e_score * 0.60) + (v_score * 0.25) + (completeness * 0.15)
    return round(combined * 100, 1)


async def recommendation_agent(state: AgentState) -> AgentState:
    scored = state.get("scored_schemes", [])
    completeness = state.get("profile_completeness", 0.5)

    if not scored:
        return {**state, "ranked_schemes": []}

    for item in scored:
        item["combined_score"] = _combined_score(item, completeness)

    scored.sort(key=lambda x: x["combined_score"], reverse=True)
    return {**state, "ranked_schemes": scored[:TOP_N]}
