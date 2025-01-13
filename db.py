from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB connection setup
MONGO_URI = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URI)
db = client.hubnexdb  # Replace 'my_database' with your database name

