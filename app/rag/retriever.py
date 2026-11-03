from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.db.database import get_db
from app.models import DocumentChunk
from app.rag.embedding import generate_embedding

def retrieve_chunks(
    question: str,
    db: Session,
    top_k: int = 3
):
    
    # Converting the question into embedding
    query_embedding = generate_embedding(
        question,
        task_type="RETRIEVAL_QUERY"
    )
    
    results = db.query(DocumentChunk).order_by(DocumentChunk.embedding.cosine_distance(query_embedding)).limit(top_k).all()
    
    # it returns the top three least cosine distane related chunks
    return results