from fastapi import FastAPI, HTTPException
from bson import ObjectId
from datetime import datetime
from typing import List
import requests
from .database import notes_collection
from .schemas import NoteCreate, NoteResponse, ChatRequest
from . import utils
from .config import Config

app = FastAPI()

@app.post("/notes/", response_model=NoteResponse)
def create_note(note: NoteCreate):
    note_data = note.dict()
    note_data["createdAt"] = datetime.utcnow()
    note_data["modifiedAt"] = datetime.utcnow()
    
    note_id = str(notes_collection.insert_one(note_data).inserted_id)
    
    utils.add_note_to_index(note_id, note.content)
    
    return NoteResponse(id=note_id, **note_data)

@app.get("/notes/search/", response_model=List[NoteResponse])
def search_notes(query: str):
    note_ids = utils.search_notes(query, similarity_threshold=0.3)
    
    notes = []
    for note_id in note_ids:
        note = notes_collection.find_one({"_id": ObjectId(note_id)})
        if note:
            notes.append(NoteResponse(
                id=str(note["_id"]),
                title=note["title"],
                content=note["content"],
                createdAt=note["createdAt"],
                modifiedAt=note["modifiedAt"]
            ))
    
    return notes

@app.post("/chat/")
def chat_with_rasa(request: ChatRequest):
    response = requests.post(
        Config.RASA_API_URL,
        json={"sender": "user", "message": request.message}
    )
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to communicate with Rasa")
    
    rasa_response = response.json()
    return {"response": rasa_response}