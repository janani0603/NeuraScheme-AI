from motor.motor_asyncio import AsyncIOMotorClient

from app.config.settings import settings

client = AsyncIOMotorClient(settings.MONGODB_URI)
db = client[settings.DATABASE_NAME]


async def connect_to_mongodb():
    try:
        await client.admin.command("ping")
        print("✅ Connected to MongoDB Atlas")
    except Exception as e:
        print("❌ MongoDB Connection Failed")
        print(e)


async def close_mongodb_connection():
    client.close()
