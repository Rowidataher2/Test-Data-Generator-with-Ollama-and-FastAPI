from sqlalchemy.orm import Session
from . import models, schemas

def create_request(db: Session, req: schemas.RequestCreate):
    db_req = models.Request(
        user_id=req.user_id,
        user_request=req.user_request,
        messages=req.messages,
        response=req.response,
    )
    db.add(db_req)
    db.commit()
    db.refresh(db_req)
    return db_req

def get_requests(db: Session, user_id: int, limit: int = 10):
    return (
        db.query(models.Request)
        .filter(models.Request.user_id == user_id)
        .order_by(models.Request.created_at.desc())
        .limit(limit)
        .all()
    )
