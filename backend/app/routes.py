# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from .database import SessionLocal
# from . import crud, schemas

# router = APIRouter()

# # Dependency to get DB session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @router.post("/requests/", response_model=schemas.RequestOut)
# def create_request(request: schemas.RequestCreate, db: Session = Depends(get_db)):
#     return crud.create_request(db, request)

# @router.get("/requests/", response_model=list[schemas.RequestOut])
# def read_requests(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     return crud.get_requests(db, skip=skip, limit=limit)
##################################################


#code of llama

# backend/app/routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import crud, schemas

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/requests/", response_model=schemas.RequestOut)
def create_request(request: schemas.RequestCreate, db: Session = Depends(get_db)):
    return crud.create_request(db, request)

@router.get("/requests/", response_model=list[schemas.RequestOut])
def read_requests(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_requests(db, skip=skip, limit=limit)
