# fastapi_backend.py
 
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware

# Import your existing LangGraph chatbot & retrieve function
from .backEnd import chatbot, retrieve_all_threads
from langchain_core.messages import HumanMessage

app = FastAPI(title="Medical Assistant Chatbot API")

# Allow cross-origin requests (needed if Streamlit frontend calls the API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------- Request/Response Models ----------------------

class ChatRequest(BaseModel):
    message: str
    thread_id: Optional[str] = None

class ChatResponse(BaseModel):
    thread_id: str
    assistant: str

# ---------------------- Endpoints ----------------------

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    if not req.message:
        raise HTTPException(status_code=400, detail="Message is required")

    # Generate a thread ID if not provided
    thread_id = req.thread_id or str(uuid4())

    # Build the human message for LangGraph
    human_msg = HumanMessage(content=req.message)

    CONFIG = {
        "configurable": {"thread_id": thread_id},
        "metadata": {"thread_id": thread_id},
        "run_name": "chat_turn",
    }

    # Call your LangGraph chatbot (preserves all nodes, edges, RAG, Pinecone, LLM)
    assistant_parts = []
    try:
        for msg_chunk, metadata in chatbot.stream(
            {"messages": [human_msg]},
            config=CONFIG,
            stream_mode='messages'
        ):
            assistant_parts.append(msg_chunk.content)

        assistant_text = "".join(assistant_parts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot error: {e}")

    return ChatResponse(thread_id=thread_id, assistant=assistant_text)

@app.get("/threads")
def get_threads():
    """Return all existing conversation thread IDs"""
    threads = retrieve_all_threads()
    return {"threads": threads}

# ---------------------- Run Uvicorn ----------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fastapi_backend:app", host="0.0.0.0", port=8000, reload=True)
