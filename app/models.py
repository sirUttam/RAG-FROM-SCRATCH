import uuid

from sqlalchemy import Column, String, UUID, Integer, Text, ForeignKey
from app.db.base import Base
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import relationship

class Document(Base):
    __tablename__ = "documents"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    
    filename = Column(String, nullable=False)

    file_path = Column(String, nullable=False)
    
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")

    
    
    
class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    
    id = Column(Integer, primary_key=True, autoincrement=True)

    document_id = Column(
        UUID(as_uuid=True),
        ForeignKey("documents.id"),
        nullable=False
    )
    
    content = Column(Text, nullable=False )
    
    page_number = Column(Integer)

    embedding = Column(Vector(768))
    
    document = relationship("Document", back_populates="chunks")
    
    
