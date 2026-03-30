"""
FastAPI Backend main entrypoint.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth.router import router as auth_router
from app.backend.routes.chat import router as chat_router
from app.backend.routes.files import router as file_router
import uvicorn

app = FastAPI(
    title="Global Tax Analyzer API",
    description="Backend for a multi-country RAG-based Tax Chatbot",
    version="1.0.0"
)

# CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your Streamlit front-end URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(file_router)

@app.get("/")
async def root():
    return {"message": "Global Tax Analyzer Backend API is running."}

if __name__ == "__main__":
    # Run the application
    uvicorn.run("app.backend.main:app", host="0.0.0.0", port=8000, reload=True)
