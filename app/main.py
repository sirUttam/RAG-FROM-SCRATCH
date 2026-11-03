from fastapi import FastAPI
from app.db.base import Base
from app.db.database import engine
from app import models
from app.routes.documents import router as document_router

app = FastAPI(title="pure rag api")
app.include_router(document_router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Pure RAG API is running"}
