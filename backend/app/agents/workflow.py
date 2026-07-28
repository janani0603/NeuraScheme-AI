import logging
from datetime import datetime, UTC
from langgraph.graph import StateGraph, END

from app.agents.profile_agent import AgentState, profile_agent
from app.agents.retrieval_agent import retrieval_agent
from app.agents.eligibility_agent import eligibility_agent
from app.agents.recommendation_agent import recommendation_agent
from app.agents.explanation_agent import explanation_agent
from app.database.connection import db
from app.models.recommendation import new_recommendation_document

logger = logging.getLogger(__name__)


def _should_continue(state: AgentState) -> str:
    """Stop the graph early if profile is invalid or no candidates found."""
    if not state.get("profile_valid"):
        return END
    if state.get("error"):
        return END
    return "continue"


def _has_candidates(state: AgentState) -> str:
    if not state.get("candidates"):
        return END
    return "continue"


def _has_scored(state: AgentState) -> str:
    if not state.get("scored_schemes"):
        return END
    return "continue"


def build_recommendation_graph() -> StateGraph:
    graph = StateGraph(AgentState)

    graph.add_node("profile", profile_agent)
    graph.add_node("retrieval", retrieval_agent)
    graph.add_node("eligibility", eligibility_agent)
    graph.add_node("recommendation", recommendation_agent)
    graph.add_node("explanation", explanation_agent)

    graph.set_entry_point("profile")

    graph.add_conditional_edges("profile", _should_continue, {"continue": "retrieval", END: END})
    graph.add_conditional_edges("retrieval", _has_candidates, {"continue": "eligibility", END: END})
    graph.add_conditional_edges("eligibility", _has_scored, {"continue": "recommendation", END: END})
    graph.add_edge("recommendation", "explanation")
    graph.add_edge("explanation", END)

    return graph.compile()


# Compiled graph — singleton
_graph = None


def get_graph():
    global _graph
    if _graph is None:
        _graph = build_recommendation_graph()
    return _graph


async def run_recommendation_pipeline(profile: dict, user_id: str) -> dict:
    """
    Run the full LangGraph recommendation pipeline.
    Saves results to MongoDB and returns formatted output.
    """
    logger.info(f"Pipeline starting for user {user_id}")
    initial_state: AgentState = {
        "user_id": user_id,
        "profile": profile,
        "profile_valid": False,
        "profile_completeness": 0.0,
        "candidates": [],
        "scored_schemes": [],
        "ranked_schemes": [],
        "explanations": {},
        "final_recommendations": [],
        "error": None,
    }

    graph = get_graph()
    logger.info("Pipeline: invoking graph")
    final_state = await graph.ainvoke(initial_state)
    logger.info(f"Pipeline: graph complete, ranked={len(final_state.get('ranked_schemes', []))}")

    ranked = final_state.get("ranked_schemes", [])
    explanations = final_state.get("explanations", {})
    completeness = final_state.get("profile_completeness", 0.0)

    # Build final recommendation list
    results = []
    for item in ranked:
        scheme = item["scheme"]
        slug = scheme.get("slug", "")
        results.append({
            "id": str(scheme.get("_id", "")),
            "scheme_name": scheme.get("scheme_name", ""),
            "slug": slug,
            "level": scheme.get("level", ""),
            "schemeCategory": scheme.get("schemeCategory", []),
            "tags": scheme.get("tags", []),
            "benefits": scheme.get("benefits", ""),
            "documents": scheme.get("documents", ""),
            "details": scheme.get("details", ""),
            "eligibility_score": item["eligibility_score"],
            "confidence_score": item["confidence_score"],
            "matched_conditions": item["matched_conditions"],
            "missing_conditions": item["missing_conditions"],
            "explanation": explanations.get(slug, ""),
            "generatedAt": datetime.now(UTC).isoformat(),
        })

    # Persist to MongoDB
    if results and user_id:
        await db["recommendations"].delete_many({"userId": user_id})
        docs = [
            new_recommendation_document(
                user_id=user_id,
                scheme_id=r["id"],
                scheme_name=r["scheme_name"],
                slug=r["slug"],
                eligibility_score=r["eligibility_score"],
                confidence_score=r["confidence_score"],
                matched_conditions=r["matched_conditions"],
                missing_conditions=r["missing_conditions"],
                explanation=r["explanation"],
            )
            for r in results[:50]
        ]
        await db["recommendations"].insert_many(docs)

    return {
        "total": len(results),
        "profile_completeness": round(completeness * 100, 1),
        "profile_valid": final_state.get("profile_valid", False),
        "error": final_state.get("error"),
        "recommendations": results[:50],
    }
