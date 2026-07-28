import asyncio
import logging
from app.agents.profile_agent import AgentState
from app.agents.gemini_client import generate
from app.agents.prompts import explanation_prompt

logger = logging.getLogger(__name__)

EXPLAIN_TOP_N = 3
EXPLAIN_TIMEOUT = 8


async def _generate_explanation(scheme: dict, profile: dict, matched: list, missing: list, score: float) -> tuple:
    slug = scheme.get("slug", "")
    try:
        prompt = explanation_prompt(scheme, profile, matched, missing)
        explanation = await asyncio.wait_for(generate(prompt, temperature=0.4), timeout=EXPLAIN_TIMEOUT)
        return slug, explanation
    except Exception as e:
        logger.warning(f"Explanation failed for {slug}: {e}")
        return slug, _fallback_explanation(matched, missing, score)


async def explanation_agent(state: AgentState) -> AgentState:
    ranked = state.get("ranked_schemes", [])
    profile = state.get("profile", {})

    # Pre-fill all with fast fallback — guarantees results even if Groq fails
    explanations = {}
    for item in ranked:
        slug = item["scheme"].get("slug", "")
        explanations[slug] = _fallback_explanation(
            item.get("matched_conditions", []),
            item.get("missing_conditions", []),
            item["eligibility_score"]
        )

    # Try Groq only for top 3, override fallback if successful
    top = ranked[:EXPLAIN_TOP_N]
    tasks = [
        _generate_explanation(
            item["scheme"], profile,
            item.get("matched_conditions", []),
            item.get("missing_conditions", []),
            item["eligibility_score"]
        )
        for item in top
    ]
    top_results = await asyncio.gather(*tasks)
    explanations.update(dict(top_results))

    return {**state, "explanations": explanations}


def _fallback_explanation(matched: list, missing: list, score: float) -> str:
    if score >= 75:
        verdict = "You are likely eligible for this scheme."
    elif score >= 50:
        verdict = "You may partially qualify for this scheme."
    else:
        verdict = "You may not meet all requirements for this scheme."

    matched_str = "; ".join(matched) if matched else "No strong matches identified"
    missing_str = "; ".join(missing) if missing else "No major gaps identified"
    return f"{verdict} Matched: {matched_str}. Gaps: {missing_str}."
