from pydantic import BaseModel
from datetime import datetime

class NoteCreate(BaseModel):
    title: str
    content: str

class NoteResponse(BaseModel):
    id: str
    title: str
    content: str
    createdAt: datetime
    modifiedAt: datetime

class ChatRequest(BaseModel):
    message: str