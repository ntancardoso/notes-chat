from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    MONGO_URL = os.getenv("MONGO_URL")
    FAISS_INDEX_DIMENSION = int(os.getenv("FAISS_INDEX_DIMENSION", 384))
    RASA_API_URL = os.getenv("RASA_API_URL")