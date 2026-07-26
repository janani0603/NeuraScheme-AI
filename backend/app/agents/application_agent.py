import logging
from datetime import datetime, UTC
from app.agents.gemini_client import generate
from app.agents.prompts import assistant_prompt
from app.database.connection import db

logger = logging.getLogger(__name__)

MAX_HISTORY = 10  # Max messages to include in context


async def application_agent(
    user_id: str,
    question: str,
    conversation_id: str | None,
    scheme_slugs: list[str] | None = None,
) -> dict:
    """
    Answers citizen questions about schemes using only verified scheme data.
    Maintains conversation history in MongoDB.
    """
    # Load scheme context
    scheme_context = await _build_scheme_context(scheme_slugs)

    # Load conversation history
    history_text, conversation_id = await _load_history(user_id, conversation_id)

    # Generate response
    try:
        prompt = assistant_prompt(question, scheme_context, history_text)
        response = await generate(prompt, temperature=0.3)
    except RuntimeError as e:
        logger.error(f"Application agent Gemini error: {e}")
        response = "I'm currently unable to process your request. Please try again shortly."

    # Save to conversation history
    await _save_message(user_id, conversation_id, question, response, scheme_slugs)

    return {
        "conversation_id": conversation_id,
        "question": question,
        "response": response,
    }


async def _build_scheme_context(scheme_slugs: list[str] | None) -> str:
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
        # Create new conversation
        from bson import ObjectId
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
    scheme_slugs: list[str] | None,
) -> None:
    message = {
        "question": question,
        "response": response,
        "scheme_slugs": scheme_slugs or [],
        "timestamp": datetime.now(UTC),
    }
    await db["conversations"].update_one(
        {"_id": conversation_id, "userId": user_id},
        {
            "$push": {"messages": message},
            "$set": {"updatedAt": datetime.now(UTC)},
        },
    )
