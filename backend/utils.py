import faiss
import pickle
from sentence_transformers import SentenceTransformer
from .config import Config
import os

# Load a pre-trained sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize FAISS index
dimension = Config.FAISS_INDEX_DIMENSION
base_index = faiss.IndexFlatL2(dimension)
index = faiss.IndexIDMap(base_index)  # Wrap the base index to support IDs

# Mapping between MongoDB note_id (string) and FAISS note_id (integer)
note_id_mapping = {}
current_id = 0  # Counter for FAISS IDs

# File paths for saving FAISS index and mapping
FAISS_INDEX_FILE = "faiss_index.index"
MAPPING_FILE = "note_id_mapping.pkl"

def save_faiss_index():
    faiss.write_index(index, FAISS_INDEX_FILE)
    with open(MAPPING_FILE, "wb") as f:
        pickle.dump((note_id_mapping, current_id), f)

def load_faiss_index():
    global index, note_id_mapping, current_id
    if os.path.exists(FAISS_INDEX_FILE):
        index = faiss.read_index(FAISS_INDEX_FILE)
    if os.path.exists(MAPPING_FILE):
        with open(MAPPING_FILE, "rb") as f:
            note_id_mapping, current_id = pickle.load(f)

load_faiss_index()

def add_note_to_index(note_id: str, text: str):
    global current_id
    embedding = model.encode([text])
    index.add_with_ids(embedding, [current_id])
    note_id_mapping[current_id] = note_id
    save_faiss_index()

def search_notes(query: str, k=5, similarity_threshold=0.5):
    query_embedding = model.encode([query])
    distances, ids = index.search(query_embedding, k)
    
    valid_note_ids = [
        note_id_mapping[note_id]
        for note_id, distance in zip(ids[0], distances[0])
        if note_id != -1 and note_id in note_id_mapping and (1 - distance) > similarity_threshold
    ]
    
    return valid_note_ids