# Test Data Generator (FastAPI + Next.js + Mistral 7B)

This project is a **Test Data Generator** that allows users to request schemas in natural language and generate realistic test data.  
It uses **FastAPI** (backend), **Next.js** (frontend), **PostgreSQL** for persistence, and **Mistral 7B** served via **Ollama** for data generation.

---

## 1. 🚀 Features
- Natural language schema definition (e.g., "Create a cars table with car_id, color, and brand with 5 rows").
- Generates realistic test data using **Mistral 7B** through **Ollama**.
- Stores all conversations and outputs in a PostgreSQL table (`requests`).
- Provides a simple chat-like frontend built with **Next.js**.
- History retrieval endpoint for previous user requests.

---

## 2.🛠️ Tech Stack
- **Backend:** FastAPI, SQLAlchemy, Pydantic  
- **Frontend:** Next.js (React, TypeScript)  
- **Database:** PostgreSQL (`datajar_agent` with `requests` table)  
- **LLM:** Mistral 7B via Ollama  
- **Other:** Requests (Python HTTP client)  

---

## 3.⚙️ Setup Instructions

### 1. Prerequisites
- Python 3.11+  
- Node.js (v18+) and npm  
- PostgreSQL running locally  
- Ollama installed with Mistral 7B model  

---

## 4. Clone Repository
```bash
git clone https://github.com/your-username/test-data-generator.git
cd test-data-generator
```
## 5.Database Setup

Create the PostgreSQL database and table:
```psql
CREATE DATABASE datajar_agent;
\c datajar_agent;
```
```psql
CREATE TABLE requests (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    user_request TEXT NOT NULL,
    messages JSONB NOT NULL,
    response JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```
## 6. Backend Setup

Navigate to the backend folder and install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

Run the FastAPI backend (on port 8001 for frontend compatibility):
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

The API will be available at:
👉 http://127.0.0.1:8001/docs

## 7. Frontend Setup

Navigate to the frontend folder and install dependencies:
```bash
cd frontend
npm install
```

Run the Next.js frontend:
```bash
npm run dev
```

The app will be available at:
👉 http://localhost:3000

## 8. Ollama Setup (Mistral 7B)

Install Ollama
 and pull the Mistral model:
```bash
ollama pull mistral:7b
```

Start Ollama in the background (it listens on http://localhost:11434 by default):
```bash
ollama run mistral:7b
```

✅ Testing the Backend (Swagger UI)

Instead of using curl, you can easily test your backend API with Swagger:

1.Open your browser and go to:
👉 http://127.0.0.1:8001/docs

2.Find the POST /chat endpoint.

3.Click "Try it out", then provide this sample request body:
```json
{
  "user_id": 1,
  "user_request": "Create a cars table with car_id, color, and brand with 3 rows",
  "messages": []
}
```

4.Click "Execute" and check the generated test data in the response.

📊 Example Output

Example response when generating a cars table:
```json
{
  "schema": {
    "table": "cars",
    "columns": ["car_id", "color", "brand"]
  },
  "rows": [
    [1, "Red", "Toyota"],
    [2, "Blue", "Ford"],
    [3, "Black", "BMW"]
  ]
}
```
✅ Frontend Test

1.Open http://localhost:3000

2.Enter:

Create a cars table with car_id, color, and brand with 3 rows


3.Click Send.

Expected output in UI:
```json
Here are 3 example rows for your schema:
[
  {
    "car_id": 1,
    "color": "red",
    "brand": "Ford"
  },
  {
    "car_id": 2,
    "color": "blue",
    "brand": "Toyota"
  },
  {
    "car_id": 3,
    "color": "silver",
    "brand": "Honda"
  }
]
```

✅ How to Test /history/{user_id} in Swagger UI


1.Open Swagger UI in your browser:

    http://127.0.0.1:8001/docs


2.Look for the GET /history/{user_id} endpoint in the docs.

3.Expand it, and you will see two parameters:

          user_id  → enter 1

          limit  → enter 5

4.Click "Try it out", then "Execute".

You should see the response JSON with the last 5 requests for user_id=1.
