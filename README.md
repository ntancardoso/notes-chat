# Notes App with Chatbot Integration

This project is a **Notes App** that allows users to store and retrieve notes using a **chatbot interface**. The app is built with **FastAPI** for the backend, **MongoDB** for data storage, and **Rasa** for the chatbot functionality. It also uses **FAISS** for semantic search to retrieve notes based on natural language queries.

## Features

- **Store Notes**: Add notes with a title and content.
- **Retrieve Notes**: Search for notes using natural language queries.
- **Chatbot Integration**: Interact with the app using a conversational chatbot.
- **Semantic Search**: Find relevant notes using FAISS for semantic similarity.

## Technologies Used

- **Backend**: FastAPI
- **Database**: MongoDB
- **Chatbot**: Rasa
- **Semantic Search**: FAISS
- **Embeddings**: Sentence Transformers

## Getting Started

### Prerequisites

- Python 3.10+
- MongoDB
- Rasa

### Installation

1. Clone the repository:
    ```
    git clone https://github.com/ntancardoso/notes-chat.git
    cd notes-chat
    ```

2. Create a virtual environment and install dependencies:
    ```
    pip install -r requirements.txt
    ```

3. Set up environment variables: Create a .env file in the root directory. You can copy from .env.sample

4. Start the FastAPI backend:
    ```
    uvicorn backend.main:app --reload
    ```

5. Start the Rasa server:
    ```
    rasa run --enable-api
    ```

6. Start the Rasa action server:
   ```
   rasa run actions
    ```

### Usage
- Add a Note:
    ```
    curl -X POST "http://localhost:8000/notes/" -H "Content-Type: application/json" -d '{"title": "MySQL User", "content": "To create a user in MySQL, use: CREATE USER username@localhost IDENTIFIED BY password"}'
    ```

- Search for Notes:
    ```
    curl "http://localhost:8000/notes/search/?query=how%20create%20user%20in%20mysql?"
    ```

- Chat with the Bot:
    ```
    curl -X POST "http://localhost:8000/chat/" -H "Content-Type: application/json" -d '{"message": "How do I create a user in MySQL?"}'
    ```

**Note:** This project is designed for learning and experimentation. For production use, consider adding authentication, error handling, and additional security measures.