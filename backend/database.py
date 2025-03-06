from pymongo import MongoClient
from .config import Config

client = MongoClient(Config.MONGO_URL)
db = client.db_notes
notes_collection = db.notes