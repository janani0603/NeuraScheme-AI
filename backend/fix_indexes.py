import asyncio

async def main():
    from motor.motor_asyncio import AsyncIOMotorClient
    from app.config.settings import settings

    client = AsyncIOMotorClient(settings.MONGODB_URI)
    db = client[settings.DATABASE_NAME]

    indexes = await db["schemes"].index_information()
    lines = []
    text_indexes = []

    for name, info in indexes.items():
        key = info.get("key", [])
        lines.append(f"{name}: {key}")
        if isinstance(key, list):
            if any(v == "text" for _, v in key):
                text_indexes.append(name)
        elif isinstance(key, dict):
            if any(v == "text" for v in key.values()):
                text_indexes.append(name)

    lines.append(f"\nText indexes: {text_indexes}")

    if len(text_indexes) > 1:
        for name in text_indexes[1:]:
            await db["schemes"].drop_index(name)
            lines.append(f"Dropped: {name}")
    elif len(text_indexes) == 0:
        await db["schemes"].create_index(
            [("scheme_name", "text"), ("details", "text"), ("eligibility", "text")],
            name="scheme_text_index"
        )
        lines.append("Created text index")
    else:
        lines.append("OK - only one text index")

    client.close()
    with open("idx_result.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

asyncio.run(main())
