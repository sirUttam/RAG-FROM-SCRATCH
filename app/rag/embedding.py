import os

from google import genai
from dotenv import load_dotenv
from google.genai import types

load_dotenv()


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_embedding(
    text: str,
    task_type: str = "RETRIEVAL_DOCUMENT"
):
    
    response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=text,
            config=types.EmbedContentConfig(
                task_type=task_type,
                output_dimensionality=768
            )
            
    )

    return response.embeddings[0].values
    