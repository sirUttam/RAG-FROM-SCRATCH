from pathlib import Path
from uuid import uuid4
from fastapi import APIRouter, UploadFile, HTTPException, File, Depends
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.models import Document, DocumentChunk
from app.rag.extractor import extract_pdf
from app.rag.chunker import chunk_text
from app.rag.embedding import generate_embedding
from app.rag.retriever import retrieve_chunks
from app.schemas import SearchRequest
from app.rag.generator import generate_answer

router = APIRouter(prefix='/documents', tags=["Documents"])


UPLOAD_DIR = Path('uploads')
UPLOAD_DIR.mkdir(exist_ok=True)



# Upload endpoint POST ---------------------------------------------------------------
@router.post("/upload")
def upload_document(uploaded_pdf: UploadFile = File(...), db: Session = Depends(get_db)):
    
    if not uploaded_pdf.filename or not uploaded_pdf.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )
        
    file_path = UPLOAD_DIR / f"{uuid4()}.pdf"
    
    # Read bytes from the uploaded PDF
    pdf_content = uploaded_pdf.file.read()
    
    # Save those bytes into a new PDF
    with open(file_path, "wb") as destination:
        destination.write(pdf_content)
        
    # Extracted text comes here
    extracted_text = extract_pdf(file_path)
    
    # Chunks are imported here
    chunks = chunk_text(extracted_text, 500, 50)
    
    # for i, chunk in enumerate(chunks):
    #     print("_________________________________________________________")
    #     print(f"Chunk{i+1}:")
    #     print(chunk)
    #     print("___________________________________________________________")
    
    # Now comes the turn of embeddings
    chunk_embeddings = []

    for chunk in chunks:
        embedding = generate_embedding(chunk)
        chunk_embeddings.append(embedding)    
    
    # Saving document in the postgresql
    document = Document(
        filename = uploaded_pdf.filename,
        file_path = str(file_path)
    )

    db.add(document)
    db.commit()
    db.refresh(document)
    
    # Saving document chunks and embeddings in the postgresql
    for chunk, embedding in zip(chunks, chunk_embeddings):
        document_chunk = DocumentChunk(
            document_id = document.id,
            content = chunk,
            embedding = embedding
        )
        
        db.add(document_chunk)
    db.commit()

    return {
        "message": "PDF uploaded successfully",
        "document_id": document.id,
        "filename": document.filename
    }
    
    
    
    
# Search endpoint POST ---------------------------------------------------------------------------

@router.post("/search")
def search_documents(
    request: SearchRequest,
    db: Session = Depends(get_db)
):
    
    print("STEP 1: Request received", flush=True)
    
    chunks = retrieve_chunks(request.question, db)
    
    print("STEP 2: Retrieval completed", flush=True)
    if not chunks:
        return{
            "answer": "No documents found"
        }
    
    answer = generate_answer(request.question, chunks)
    
    print("STEP 3: Generation completed", flush=True)
    

    return {
        "question": request.question,
        "answer": answer
    }