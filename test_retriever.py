from app.rag.retriever import retrieve_chunks
from app.db.database import SessionLocal


with SessionLocal() as db:
    
    question = "What work experience does this candidate have?"
    
    
    result = retrieve_chunks(
        question,
        db
    )
    
    for chunk in result:
        print(f"Chunk ID: {chunk.id}")
        print("------------------------")
        print(f"Document ID: {chunk.document_id}")
        print("------------------------")
        print(f"Content: {chunk.content}")
        print("------------------------")
