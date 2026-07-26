import json
import logging
from app.agents.profile_agent import AgentState
from app.agents.gemini_client import generate
from app.agents.prompts import ranking_prompt

logger = logging.getLogger(__name__)

TOP_N = 50          # Max recommendations to return
GEMINI_RERANK_N = 20  # Only re-rank top N with Gemini


def _combined_score(item: dict, completeness: float) -> float:
    """
    Weighted combination:
    - Eligibility score: 60%
    - Vector similarity: 25%
    - Profile completeness bonus: 15%
    """
    e_score = item["eligibility_score"] / 100
    v_score = float(item.get("vector_score", 0.0))
    combined = (e_score * 0.60) + (v_score * 0.25) + (completeness * 0.15)
    return round(combined * 100, 1)


async def recommendation_agent(state: AgentState) -> AgentState:
    """
    Ranks scored schemes using combined scoring.
    Uses Gemini to re-rank the top candidates for better relevance.
    """
    scored = state.get("scored_schemes", [])
    profile = state.get("profile", {})
    completeness = state.get("profile_completeness", 0.5)

    if not scored:
        return {**state, "ranked_schemes": []}

    # Compute combined score for all
    for item in scored:
        item["combined_score"] = _combined_score(item, completeness)

    scored.sort(key=lambda x: x["combined_score"], reverse=True)

    # Gemini re-ranking for top candidates only
    top = scored[:GEMINI_RERANK_N]
    rest = scored[GEMINI_RERANK_N:]

    try:
        schemes_summary = "\n".join(
            f"{item['scheme'].get('slug', '')}: {item['scheme'].get('scheme_name', '')}"
            for item in top
        )
        prompt = ranking_prompt(schemes_summary, profile)
        raw = await generate(prompt, temperature=0.1)

        # Parse slug order from Gemini
        slug_order = json.loads(raw)
        if isinstance(slug_order, list) and slug_order:
            slug_index = {slug: i for i, slug in enumerate(slug_order)}
            top.sort(key=lambda x: slug_index.get(x["scheme"].get("slug", ""), 999))
            logger.info("Gemini re-ranking applied successfully")

    except Exception as e:
        logger.warning(f"Gemini re-ranking failed, using combined score order: {e}")

    ranked = (top + rest)[:TOP_N]
    return {**state, "ranked_schemes": ranked}
