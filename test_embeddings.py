from app.rag.embedding import generate_embedding

text = "FastAPI is a Python framework for building APIs."

embedding = generate_embedding(text)

print(f"embeddings: {embedding}")
print("________________________________")
print(f"Dimensions: {len(embedding)}")
print("_______________________________")
