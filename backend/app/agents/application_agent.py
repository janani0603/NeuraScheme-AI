import json
import asyncio
import logging
from datetime import datetime, UTC
from bson import ObjectId

from app.agents.gemini_client import generate
from app.agents.prompts import intent_router_prompt, synthesis_prompt, assistant_prompt
from app.database.connection import db

logger = logging.getLogger(__name__)

MAX_HISTORY = 10


# ── Intent Router ─────────────────────────────────────────────────────────────

async def _route_intent(question: str, history: str) -> dict:
    """Classify the question and decide which agents to invoke."""
    try:
        prompt = intent_router_prompt(question, history)
        raw = await generate(prompt, temperature=0.1)
        parsed = json.loads(raw)
        return {
            "intents": parsed.get("intents", ["general"]),
            "scheme_slugs_mentioned": parsed.get("scheme_slugs_mentioned", []),
            "needs_profile": parsed.get("needs_profile", False),
        }
    except Exception as e:
        logger.warning(f"Intent routing failed, defaulting to general: {e}")
        return {"intents": ["general"], "scheme_slugs_mentioned": [], "needs_profile": False}


# ── Agent Runners ─────────────────────────────────────────────────────────────

async def _run_recommendations(user_id: str, profile: dict) -> str:
    """Run the full recommendation pipeline and return a text summary."""
    try:
        from app.agents.workflow import run_recommendation_pipeline
        result = await run_recommendation_pipeline(profile, user_id)
        recs = result.get("recommendations", [])[:5]
        if not recs:
            return "RECOMMENDATIONS AGENT: No matching schemes found for your profile."
        lines = [f"RECOMMENDATIONS AGENT: Found {result['total']} matching schemes. Top 5:"]
        for r in recs:
            lines.append(
                f"- {r['scheme_name']} (Eligibility: {r['eligibility_score']}%) — {r['explanation'][:120]}"
            )
        return "\n".join(lines)
    except Exception as e:
        logger.warning(f"Recommendations agent failed: {e}")
        return "RECOMMENDATIONS AGENT: Could not fetch recommendations at this time."


async def _run_comparison(scheme_slugs: list[str], profile: dict) -> str:
    """Run comparison agent and return text summary."""
    try:
        from app.agents.comparison_agent import comparison_agent
        result = await comparison_agent(scheme_slugs=scheme_slugs, profile=profile)
        if "error" in result:
            return f"COMPARISON AGENT: {result['error']}"
        lines = [f"COMPARISON AGENT: {result.get('summary', '')}"]
        for item in result.get("comparison", []):
            lines.append(
                f"- {item['scheme_name']}: {item['key_benefit']} | "
                f"Ease: {item['ease_of_apply']} | "
                f"Pros: {', '.join(item['pros'][:2])} | "
                f"Cons: {', '.join(item['cons'][:2])}"
            )
        best = result.get("best_for_user", "")
        if best:
            lines.append(f"Best for you: {best} — {result.get('reason', '')}")
        return "\n".join(lines)
    except Exception as e:
        logger.warning(f"Comparison agent failed: {e}")
        return "COMPARISON AGENT: Could not compare schemes at this time."


async def _run_documents(scheme_slugs: list[str], user_id: str) -> str:
    """Run document checker for mentioned schemes."""
    try:
        from app.agents.document_checker_agent import document_checker_agent
        # Get user's saved documents if any
        user = await db["users"].find_one({"_id": ObjectId(user_id)}, {"documents": 1})
        user_docs = user.get("documents", []) if user else []

        if not scheme_slugs:
            return "DOCUMENT AGENT: No specific scheme mentioned to check documents for."

        tasks = [document_checker_agent(slug, user_docs) for slug in scheme_slugs[:3]]
        results = await asyncio.gather(*tasks)

        lines = ["DOCUMENT AGENT:"]
        for r in results:
            if "error" not in r:
                lines.append(
                    f"- {r['scheme_name']}: Readiness {r['readiness_score']}% | "
                    f"Have: {', '.join(r['have'][:3]) or 'None'} | "
                    f"Missing: {', '.join(r['missing'][:3]) or 'None'} | "
                    f"{r['advice']}"
                )
        return "\n".join(lines)
    except Exception as e:
        logger.warning(f"Document agent failed: {e}")
        return "DOCUMENT AGENT: Could not check documents at this time."


async def _run_deadlines(scheme_slugs: list[str], user_id: str) -> str:
    """Run deadline agent for mentioned or saved schemes."""
    try:
        from app.agents.deadline_agent import deadline_agent

        # If no slugs mentioned, use user's saved recommendations
        if not scheme_slugs:
            recs = await db["recommendations"].find(
                {"userId": user_id}, {"slug": 1}
            ).limit(10).to_list(length=10)
            scheme_slugs = [r["slug"] for r in recs]

        if not scheme_slugs:
            return "DEADLINE AGENT: No schemes found to check deadlines for."

        result = await deadline_agent(user_id=user_id, scheme_slugs=scheme_slugs[:10])
        deadlines = result.get("deadlines", [])
        urgent = [d for d in deadlines if d.get("has_deadline")]

        if not urgent:
            return "DEADLINE AGENT: No upcoming deadlines found. Most schemes appear to be ongoing."

        lines = [f"DEADLINE AGENT: Found {len(urgent)} scheme(s) with deadlines:"]
        for d in urgent[:5]:
            urgency_label = {"high": "🔴 URGENT", "medium": "🟡 Soon", "low": "🟢 Low"}.get(d["urgency"], "")
            lines.append(f"- {d['scheme_name']}: {d.get('deadline_text', 'Deadline exists')} {urgency_label}")
        return "\n".join(lines)
    except Exception as e:
        logger.warning(f"Deadline agent failed: {e}")
        return "DEADLINE AGENT: Could not check deadlines at this time."


async def _run_general(question: str, scheme_slugs: list[str], history: str, history_status: str) -> str:
    """Run general scheme Q&A using scheme context."""
    try:
        scheme_context = await _build_scheme_context(scheme_slugs)
        prompt = assistant_prompt(question, scheme_context, history, history_status)
        response = await generate(prompt, temperature=0.3)
        return f"GENERAL AGENT: {response}"
    except Exception as e:
        logger.warning(f"General agent failed: {e}")
        return "GENERAL AGENT: Could not answer at this time."


# ── Main Orchestrator ─────────────────────────────────────────────────────────

async def application_agent(
    user_id: str,
    question: str,
    conversation_id: str | None,
    scheme_slugs: list[str] | None = None,
) -> dict:
    """
    Multi-agent orchestrator for the AI Assistant.
    Routes the question to relevant agents, runs them concurrently,
    then synthesizes all outputs into one unified response.
    """
    # Load conversation history
    history_text, conversation_id = await _load_history(user_id, conversation_id)
    history_status = "follow-up conversation" if history_text else "first message"

    # Step 1 — Intent routing
    routing = await _route_intent(question, history_text)
    intents = routing["intents"]
    mentioned_slugs = scheme_slugs or routing["scheme_slugs_mentioned"] or []

    logger.info(f"Intents detected: {intents} | Slugs: {mentioned_slugs}")

    # Step 2 — Load user profile if needed
    profile = {}
    if routing["needs_profile"] or "recommendations" in intents:
        user = await db["users"].find_one({"_id": ObjectId(user_id)})
        if user:
            profile = {
                "state": user.get("state"),
                "gender": user.get("gender"),
                "occupation": user.get("occupation"),
                "education": user.get("education"),
                "annual_income": user.get("annual_income"),
                "category": user.get("category"),
                "is_student": user.get("is_student", False),
                "is_farmer": user.get("is_farmer", False),
                "is_business_owner": user.get("is_business_owner", False),
                "has_disability": user.get("has_disability", False),
                "age": None,
            }

    # Step 3 — Run relevant agents concurrently
    tasks = {}

    if "recommendations" in intents:
        tasks["recommendations"] = _run_recommendations(user_id, profile)

    if "comparison" in intents and len(mentioned_slugs) >= 2:
        tasks["comparison"] = _run_comparison(mentioned_slugs, profile)

    if "documents" in intents:
        tasks["documents"] = _run_documents(mentioned_slugs, user_id)

    if "deadlines" in intents:
        tasks["deadlines"] = _run_deadlines(mentioned_slugs, user_id)

    # Always run general if it's the only intent or alongside others for context
    if "general" in intents or not tasks:
        tasks["general"] = _run_general(question, mentioned_slugs, history_text, history_status)

    # Run all selected agents concurrently
    agent_results = await asyncio.gather(*tasks.values(), return_exceptions=True)
    agent_outputs = "\n\n".join(
        str(r) for r in agent_results if not isinstance(r, Exception)
    )

    # Step 4 — Synthesize all outputs into one response
    # If only general agent ran, use its output directly (no need for extra synthesis call)
    if list(tasks.keys()) == ["general"]:
        response = agent_outputs.replace("GENERAL AGENT: ", "", 1)
    else:
        try:
            prompt = synthesis_prompt(question, agent_outputs, history_text, history_status)
            response = await generate(prompt, temperature=0.3)
        except Exception as e:
            logger.error(f"Synthesis failed: {e}")
            response = agent_outputs  # fallback: return raw agent outputs

    # Step 5 — Save to conversation history
    await _save_message(user_id, conversation_id, question, response, mentioned_slugs)

    return {
        "conversation_id": conversation_id,
        "question": question,
        "response": response,
        "agents_used": list(tasks.keys()),
    }


# ── Helpers ───────────────────────────────────────────────────────────────────

async def _build_scheme_context(scheme_slugs: list[str]) -> str:
    if not scheme_slugs:
        return "No specific schemes selected. Answer general questions about government schemes."

    docs = await db["schemes"].find(
        {"slug": {"$in": scheme_slugs}},
        {"scheme_name": 1, "benefits": 1, "eligibility": 1, "documents": 1, "application": 1}
    ).to_list(length=10)

    if not docs:
        return "No scheme information found for the selected schemes."

    parts = []
    for doc in docs:
        parts.append(
            f"SCHEME: {doc.get('scheme_name', '')}\n"
            f"Benefits: {doc.get('benefits', '')}\n"
            f"Eligibility: {doc.get('eligibility', '')}\n"
            f"Documents: {doc.get('documents', '')}\n"
            f"Application: {doc.get('application', '')}\n"
        )
    return "\n---\n".join(parts)


async def _load_history(user_id: str, conversation_id: str | None) -> tuple[str, str]:
    if conversation_id:
        conv = await db["conversations"].find_one({"_id": conversation_id, "userId": user_id})
    else:
        conv = None

    if not conv:
        new_id = str(ObjectId())
        await db["conversations"].insert_one({
            "_id": new_id,
            "userId": user_id,
            "messages": [],
            "createdAt": datetime.now(UTC),
            "updatedAt": datetime.now(UTC),
        })
        return "", new_id

    messages = conv.get("messages", [])[-MAX_HISTORY:]
    history_lines = []
    for msg in messages:
        history_lines.append(f"User: {msg.get('question', '')}")
        history_lines.append(f"Assistant: {msg.get('response', '')}")

    return "\n".join(history_lines), conversation_id


async def _save_message(
    user_id: str,
    conversation_id: str,
    question: str,
    response: str,
    scheme_slugs: list[str],
) -> None:
    await db["conversations"].update_one(
        {"_id": conversation_id, "userId": user_id},
        {
            "$push": {"messages": {
                "question": question,
                "response": response,
                "scheme_slugs": scheme_slugs or [],
                "timestamp": datetime.now(UTC),
            }},
            "$set": {"updatedAt": datetime.now(UTC)},
        },
    )
