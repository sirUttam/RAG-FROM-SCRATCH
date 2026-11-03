# Pure RAG

A simple Retrieval-Augmented Generation (RAG) project built using Python and FastAPI, without using frameworks like LangChain or LlamaIndex.

I built this project to understand how RAG works, from processing PDF documents and generating embeddings to retrieving relevant information and generating answers using an LLM.

## Features

- Upload and process PDF documents.
- Extract text from uploaded PDFs using PyMuPDF.
- Split extracted text into smaller chunks with overlap.
- Generate text embeddings using Google's Gemini API.
- Store documents, chunks, and embeddings in PostgreSQL with pgvector.
- Retrieve relevant chunks using cosine distance.
- Generate answers based on retrieved document content using Gemini.

## Tech Stack

- **Backend:** Python, FastAPI
- **Database:** PostgreSQL, pgvector
- **ORM:** SQLAlchemy
- **AI Models:** Google Gemini API
- **PDF Processing:** PyMuPDF
- **Containerization:** Docker

## How It Works

**1. Document Upload**

The user uploads a PDF through the `/documents/upload` endpoint.

- The PDF is saved locally in the `uploads` folder.
- Text is extracted using PyMuPDF.
- The extracted text is split into chunks of 500 characters with 50 characters of overlap.
- Each chunk is converted into a 768-dimensional embedding using Gemini.
- The document details, chunks, and embeddings are stored in PostgreSQL.

**2. Question Answering**

The user sends a question through the `/documents/search` endpoint.

- The question is converted into an embedding.
- PostgreSQL with pgvector searches for the most relevant chunks using cosine distance.
- The retrieved text and the question are sent to Gemini.
- Gemini generates an answer based on the retrieved content.
- FastAPI returns the generated answer.

The current implementation searches across all uploaded documents.

## API Endpoints

| Method | Endpoint            | Description                                                             |
|---     |---                  |---                                                                      |
| POST   | `/documents/upload` | Upload a PDF, extract text, generate embeddings, and store the document |
| POST   | `/documents/search` | Retrieve relevant document content and generate an answer               |

### Example Request

**POST `/documents/search`**

```json
{
  "question": "What work experience does the candidate have?"
}
```

### Example Response

```json
{
  "question": "What work experience does the candidate have?",
  "answer": "The candidate worked at a hardware store and an automobile workshop."
}
```

*The response above is an example. Actual answers depend on the uploaded documents.*

## Running the Project

**1. Clone the repository**

```bash
git clone <your-repository-url>
cd pure-rag
```

**2. Create and activate a virtual environment**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

Create a `.env` file with the following variables:

```env
GEMINI_API_KEY=your_api_key
DATABASE_URL=your_database_connection_url
```

**5. Start PostgreSQL using Docker**

```bash
docker compose up -d
```

Make sure the pgvector extension is enabled and the required database tables are created.

**6. Run the FastAPI server**

```bash
uvicorn app.main:app --reload
```

Open Swagger UI at:

http://127.0.0.1:8000/docs

You can upload PDF documents and ask questions directly through the API documentation.

## Project Purpose

This project was developed mainly for learning and understanding the basic concepts of RAG.

Instead of using ready-made RAG frameworks, I implemented the main steps using Python functions, Gemini API, FastAPI, and PostgreSQL with pgvector.

The project is intended for learning and demonstration, not production use.