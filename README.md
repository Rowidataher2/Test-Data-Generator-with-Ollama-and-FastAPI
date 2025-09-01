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
