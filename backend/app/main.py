# from fastapi import FastAPI, Depends, HTTPException, Query
# from pydantic import BaseModel, validator
# from sqlalchemy.orm import Session
# from fastapi.middleware.cors import CORSMiddleware
# import os
# import json
# import re
# import logging
# import requests
# from typing import Any, Optional

# from . import models, database, crud, schemas

# app = FastAPI()
# models.Base.metadata.create_all(bind=database.engine)

# OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
# OLLAMA_CHAT_ENDPOINT = f"{OLLAMA_URL}/api/chat"
# OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral:7b")

# def get_db():
#     db = database.SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# class GeneratePayload(BaseModel):
#     user_id: int
#     user_request: str
#     num_rows: Optional[int] = 5

#     @validator("user_request")
#     def must_have_schema(cls, v):
#         # Check it contains 'generate a schema' and 'with' for columns
#         text = v.strip().lower()
#         if "generate a schema" not in text:
#             raise ValueError("Request must contain 'Generate a schema'.")
#         if "with" not in text or not any(col.strip() for col in text.split("with")[-1].split(",")):
#             raise ValueError("You must specify at least one column after 'with'.")
#         return v


# def _extract_json_fragment(text: str) -> Optional[Any]:
#     try:
#         return json.loads(text)
#     except Exception:
#         pass

#     m = re.search(r"(\[.*\]|\{.*\})", text, flags=re.S)
#     if m:
#         frag = m.group(1)
#         try:
#             return json.loads(frag)
#         except Exception:
#             return None
#     return None


# @app.post("/generate_data")
# def generate_data(payload: GeneratePayload, db: Session = Depends(get_db)):
#     user_text = payload.user_request
#     num_rows = payload.num_rows or 5

#     prompt = (
#         f"You are a helpful test data generator.\n"
#         f"The user asked: {user_text}\n\n"
#         f"Produce exactly {num_rows} rows that match the described schema.\n"
#         "Output only valid JSON (an array of objects). No explanations, no markdown.\n"
#         "Use realistic types: integers for ids/quantities, floats for prices, ISO-8601 for datetimes, short strings for names/brands/colors.\n"
#         "Make sure keys match the field names the user mentioned.\n"
#     )

#     try:
#         r = requests.post(
#             OLLAMA_CHAT_ENDPOINT,
#             json={
#                 "model": OLLAMA_MODEL,
#                 "messages": [{"role": "user", "content": prompt}],
#                 "stream": False,
#             },
#             timeout=10000,
#         )
#         r.raise_for_status()
#         j = r.json()

#         generated_text = None
#         if isinstance(j, dict):
#             generated_text = j.get("message", {}).get("content") or j.get("response") or j.get("output") or j.get("result")
#         if not generated_text:
#             generated_text = r.text

#         parsed = _extract_json_fragment(generated_text)

#         if parsed is None:
#             # fallback generation
#             fields = [f.strip() for f in user_text.split("with")[-1].split(",") if f.strip()]
#             rows = []
#             for i in range(num_rows):
#                 row = {}
#                 for f in fields:
#                     lf = f.lower()
#                     if "id" in lf:
#                         row[f] = i + 1
#                     elif "price" in lf or "cost" in lf:
#                         row[f] = round(100.0 + i * 10.5, 2)
#                     elif "quantity" in lf or "qty" in lf:
#                         row[f] = (i % 10) + 1
#                     else:
#                         row[f] = f"sample_{i + 1}"
#                 rows.append(row)
#             parsed = rows if rows else {"raw": generated_text}

#         req_in = schemas.RequestCreate(
#             user_id=payload.user_id, user_request=user_text, response=parsed
#         )
#         db_req = crud.create_request(db, req_in)

#         return {"generated_data": parsed, "created_at": db_req.created_at}

#     except requests.RequestException as e:
#         logging.exception("Ollama request failed")
#         raise HTTPException(status_code=500, detail=f"Ollama request failed: {str(e)}")
#     except Exception as e:
#         logging.exception("generate_data failed")
#         raise HTTPException(status_code=500, detail=str(e))


# @app.get("/history/{user_id}")
# def get_user_history(user_id: int, db: Session = Depends(get_db), limit: int = Query(10)):
#     history = (
#         db.query(models.Request)
#         .filter(models.Request.user_id == user_id)
#         .order_by(models.Request.created_at.desc())
#         .limit(limit)
#         .all()
#     )
#     return history


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )




#######################################


# from fastapi import FastAPI, Depends, HTTPException, Query
# from sqlalchemy.orm import Session
# from fastapi.middleware.cors import CORSMiddleware
# import os, json, re, logging, requests
# from typing import Any, Optional

# from . import models, database, crud, schemas

# app = FastAPI()
# models.Base.metadata.create_all(bind=database.engine)

# OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
# OLLAMA_CHAT_ENDPOINT = f"{OLLAMA_URL}/api/chat"
# OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral:7b")

# def get_db():
#     db = database.SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# def _extract_json_fragment(text: str) -> Optional[Any]:
#     try:
#         return json.loads(text)
#     except Exception:
#         pass
#     m = re.search(r"(\[.*\]|\{.*\})", text, flags=re.S)
#     if m:
#         frag = m.group(1)
#         try:
#             return json.loads(frag)
#         except Exception:
#             return None
#     return None


# @app.post("/chat")
# def chat_with_model(payload: schemas.RequestCreate, db: Session = Depends(get_db)):
#     user_id = payload.user_id
#     user_text = payload.user_request
#     messages = payload.messages

#     # Always prepend system instruction
#     system_prompt = (
#         "You are a helpful test data generator. "
#         "Always output valid JSON when user asks for data. "
#         "Use integers for IDs, floats for prices, ISO-8601 for dates, short strings for names."
#     )
#     full_messages = [{"role": "system", "content": system_prompt}] + messages

#     try:
#         r = requests.post(
#             OLLAMA_CHAT_ENDPOINT,
#             json={"model": OLLAMA_MODEL, "messages": full_messages, "stream": False},
#             timeout=10000,
#         )
#         r.raise_for_status()
#         j = r.json()

#         generated_text = (
#             j.get("message", {}).get("content")
#             or j.get("response")
#             or j.get("output")
#             or j.get("result")
#             or r.text
#         )

#         parsed = _extract_json_fragment(generated_text)
#         # Save chat + parsed JSON (if any)
#         req_in = schemas.RequestCreate(
#             user_id=user_id,
#             user_request=user_text,
#             messages=messages,
#             response=parsed,
#         )
#         db_req = crud.create_request(db, req_in)

#         return {"messages": messages + [{"role": "assistant", "content": generated_text}],
#                 "generated_data": parsed,
#                 "created_at": db_req.created_at}

#     except Exception as e:
#         logging.exception("chat_with_model failed")
#         raise HTTPException(status_code=500, detail=str(e))


# @app.get("/history/{user_id}")
# def get_user_history(user_id: int, db: Session = Depends(get_db), limit: int = Query(10)):
#     return crud.get_requests(db, user_id=user_id, limit=limit)


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


########################33
# from fastapi import FastAPI, Depends, HTTPException, Query
# from sqlalchemy.orm import Session
# from fastapi.middleware.cors import CORSMiddleware
# import os, json, re, logging, requests
# from typing import Any, Optional, List

# from . import models, database, crud, schemas

# app = FastAPI()
# models.Base.metadata.create_all(bind=database.engine)

# # Ollama config
# OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
# OLLAMA_CHAT_ENDPOINT = f"{OLLAMA_URL}/api/chat"
# OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral:7b")


# def get_db():
#     db = database.SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# def _extract_json_fragment(text: str) -> Optional[Any]:
#     """Try to extract JSON object/array from raw model text."""
#     try:
#         return json.loads(text)
#     except Exception:
#         pass
#     m = re.search(r"(\[.*\]|\{.*\})", text, flags=re.S)
#     if m:
#         frag = m.group(1)
#         try:
#             return json.loads(frag)
#         except Exception:
#             return None
#     return None


# @app.post("/chat")
# def chat_with_model(payload: schemas.RequestCreate, db: Session = Depends(get_db)):
#     user_id = payload.user_id
#     user_text = payload.user_request
#     messages = payload.messages

#     # System instruction
#     system_prompt = (
#         "You are a helpful assistant and test data generator. "
#         "If the user asks for schema or data, output valid JSON (array of objects). "
#         "Otherwise, reply conversationally like a chatbot. "
#         "Use integers for IDs, ISO-8601 for dates, and short strings for names."
#     )
#     full_messages = [{"role": "system", "content": system_prompt}] + messages

#     try:
#         r = requests.post(
#             OLLAMA_CHAT_ENDPOINT,
#             json={"model": OLLAMA_MODEL, "messages": full_messages, "stream": False},
#             timeout=10000,
#         )
#         r.raise_for_status()
#         j = r.json()

#         generated_text = (
#             j.get("message", {}).get("content")
#             or j.get("response")
#             or j.get("output")
#             or j.get("result")
#             or r.text
#         )

#         # Try parsing JSON
#         parsed = _extract_json_fragment(generated_text)

#         # Always store valid JSON or raw text
#         if parsed is None:
#             response_to_store = {"reply": generated_text}
#         else:
#             response_to_store = parsed

#         # Save to DB
#         req_in = schemas.RequestCreate(
#             user_id=user_id,
#             user_request=user_text,
#             messages=messages,
#             response=response_to_store,
#         )
#         db_req = crud.create_request(db, req_in)

#         return {
#             "messages": messages + [{"role": "assistant", "content": generated_text}],
#             "generated_data": response_to_store,
#             "created_at": db_req.created_at,
#         }

#     except Exception as e:
#         logging.exception("chat_with_model failed")
#         raise HTTPException(status_code=500, detail=str(e))


# @app.get("/history/{user_id}")
# def get_user_history(user_id: int, db: Session = Depends(get_db), limit: int = Query(10)):
#     """Return last N chats for a given user in chat-like format."""
#     history = crud.get_requests(db, user_id=user_id, limit=limit)

#     formatted_history: List[dict] = []
#     for h in history:
#         formatted_history.append({
#             "user_request": h.user_request,
#             "messages": h.messages + [{"role": "assistant", "content": json.dumps(h.response)}],
#             "response": h.response,
#             "created_at": h.created_at,
#         })

#     return formatted_history


# # Enable CORS for frontend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
##########################333
# from fastapi import FastAPI, Depends, HTTPException, Query
# from sqlalchemy.orm import Session
# from fastapi.middleware.cors import CORSMiddleware
# import os, json, re, logging, requests
# from typing import Any, Optional, List

# from . import models, database, crud, schemas

# app = FastAPI()
# models.Base.metadata.create_all(bind=database.engine)

# # Ollama config
# OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
# OLLAMA_CHAT_ENDPOINT = f"{OLLAMA_URL}/api/chat"
# OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral:7b")


# def get_db():
#     db = database.SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# def _extract_json_fragment(text: str) -> Optional[Any]:
#     """Try to extract JSON object/array from raw model text."""
#     try:
#         return json.loads(text)
#     except Exception:
#         pass
#     m = re.search(r"(\[.*\]|\{.*\})", text, flags=re.S)
#     if m:
#         frag = m.group(1)
#         try:
#             return json.loads(frag)
#         except Exception:
#             return None
#     return None


# @app.post("/chat")
# def chat_with_model(payload: schemas.RequestCreate, db: Session = Depends(get_db)):
#     user_id = payload.user_id
#     user_text = payload.user_request
#     messages = payload.messages

#     # Detect if schema request
#     is_schema_request = "schema" in user_text.lower() or "table" in user_text.lower()

#     if is_schema_request:
#         system_prompt = (
#             "You are a test data generator. "
#             "The user will describe a schema (fields, table, columns). "
#             "DO NOT generate the schema itself. Instead, generate ONE sample data row. "
#             "Return ONLY valid JSON object (not array) matching the schema. "
#             "Use integers for IDs, short strings for names, realistic numbers."
#         )
#     else:
#         system_prompt = (
#             "You are a helpful assistant chatbot. "
#             "If the user chats casually, respond conversationally. "
#             "Do not generate JSON unless explicitly asked."
#         )

#     full_messages = [{"role": "system", "content": system_prompt}] + messages

#     try:
#         r = requests.post(
#             OLLAMA_CHAT_ENDPOINT,
#             json={"model": OLLAMA_MODEL, "messages": full_messages, "stream": False},
#             timeout=10000,
#         )
#         r.raise_for_status()
#         j = r.json()

#         generated_text = (
#             j.get("message", {}).get("content")
#             or j.get("response")
#             or j.get("output")
#             or j.get("result")
#             or r.text
#         )

#         parsed = _extract_json_fragment(generated_text)

#         # Store structured response
#         if is_schema_request and parsed:
#             response_to_store = parsed
#             assistant_reply = f"Here is some example data for your schema: {json.dumps(parsed)}"
#         else:
#             response_to_store = {"reply": generated_text}
#             assistant_reply = generated_text

#         # Save to DB
#         req_in = schemas.RequestCreate(
#             user_id=user_id,
#             user_request=user_text,
#             messages=messages,
#             response=response_to_store,
#         )
#         db_req = crud.create_request(db, req_in)

#         return {
#             "messages": messages + [{"role": "assistant", "content": assistant_reply}],
#             "generated_data": response_to_store,
#             "created_at": db_req.created_at,
#         }

#     except Exception as e:
#         logging.exception("chat_with_model failed")
#         raise HTTPException(status_code=500, detail=str(e))


# @app.get("/history/{user_id}")
# def get_user_history(user_id: int, db: Session = Depends(get_db), limit: int = Query(10)):
#     """Return last N chats for a given user in chat-like format."""
#     history = crud.get_requests(db, user_id=user_id, limit=limit)

#     formatted_history: List[dict] = []
#     for h in history:
#         formatted_history.append({
#             "user_request": h.user_request,
#             "messages": h.messages + [{"role": "assistant", "content": json.dumps(h.response)}],
#             "response": h.response,
#             "created_at": h.created_at,
#         })

#     return formatted_history


# # Enable CORS for frontend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


#backend/app/main.py
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import os, json, re, logging, requests
from typing import Any, Optional, List

from . import models, database, crud, schemas

app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)

# Ollama config
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_CHAT_ENDPOINT = f"{OLLAMA_URL}/api/chat"
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral:7b")


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _extract_json_fragment(text: str) -> Optional[Any]:
    """Try to extract JSON object/array from raw model text."""
    try:
        return json.loads(text)
    except Exception:
        pass
    m = re.search(r"(\[.*\]|\{.*\})", text, flags=re.S)
    if m:
        frag = m.group(1)
        try:
            return json.loads(frag)
        except Exception:
            return None
    return None


def _extract_num_rows(user_text: str) -> int:
    """Extract requested number of rows from user text, default=1"""
    match = re.search(r"\b(\d+)\s*(rows|row|records|entries)?", user_text.lower())
    if match:
        return max(1, int(match.group(1)))
    return 1


@app.post("/chat")
def chat_with_model(payload: schemas.RequestCreate, db: Session = Depends(get_db)):
    user_id = payload.user_id
    user_text = payload.user_request
    messages = payload.messages

    # Detect if schema request
    is_schema_request = "schema" in user_text.lower() or "table" in user_text.lower()

    num_rows = 1
    if is_schema_request:
        num_rows = _extract_num_rows(user_text)

        system_prompt = (
            "You are a test data generator. "
            f"The user will describe a schema (fields, table, columns). Generate {num_rows} sample rows. "
            "Return ONLY valid JSON. "
            "If more than 1 row is requested, return a JSON array of objects. "
            "Use integers for IDs, short strings for names, realistic numbers."
        )
    else:
        system_prompt = (
            "You are a helpful assistant chatbot. "
            "If the user chats casually, respond conversationally. "
            "Do not generate JSON unless explicitly asked."
        )

    full_messages = [{"role": "system", "content": system_prompt}] + messages

    try:
        r = requests.post(
            OLLAMA_CHAT_ENDPOINT,
            json={"model": OLLAMA_MODEL, "messages": full_messages, "stream": False},
            timeout=10000,
        )
        r.raise_for_status()
        j = r.json()

        generated_text = (
            j.get("message", {}).get("content")
            or j.get("response")
            or j.get("output")
            or j.get("result")
            or r.text
        )

        parsed = _extract_json_fragment(generated_text)

        # Store structured response
        if is_schema_request and parsed:
            response_to_store = parsed
            assistant_reply = f"Here are {num_rows} example rows for your schema:\n{json.dumps(parsed, indent=2)}"
        else:
            response_to_store = {"reply": generated_text}
            assistant_reply = generated_text

        # Save to DB
        req_in = schemas.RequestCreate(
            user_id=user_id,
            user_request=user_text,
            messages=messages,
            response=response_to_store,
        )
        db_req = crud.create_request(db, req_in)

        return {
            "messages": messages + [{"role": "assistant", "content": assistant_reply}],
            "generated_data": response_to_store,
            "created_at": db_req.created_at,
        }

    except Exception as e:
        logging.exception("chat_with_model failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history/{user_id}")
def get_user_history(user_id: int, db: Session = Depends(get_db), limit: int = Query(10)):
    """Return last N chats for a given user in chat-like format."""
    history = crud.get_requests(db, user_id=user_id, limit=limit)

    formatted_history: List[dict] = []
    for h in history:
        formatted_history.append({
            "user_request": h.user_request,
            "messages": h.messages + [{"role": "assistant", "content": json.dumps(h.response)}],
            "response": h.response,
            "created_at": h.created_at,
        })

    return formatted_history


# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
