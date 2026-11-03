import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_answer(
    question: str,
    chunks: list
):
    
    context = ""

    for chunk in chunks:
        context = context + chunk.content + "\n\n"
    
    prompt = f"""
    Answer the question using only the context below.
    If the answer is not in the context, say
    "I don't have information for this question."
    
    context: {context}

    Question: {question}
    
    """
    print("GENERATOR: Sending request to Gemini", flush=True)
    
    response = client.interactions.create(
    model="gemini-3.5-flash-lite",
    input=prompt,
    store=False
    )
    
    print("GENERATOR: Gemini responded", flush=True)
    
    return response.output_text
    
