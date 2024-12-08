from sqlalchemy.orm import Session
import models

def create_client(db: Session, name: str, client_code: str):
    db_client = models.Client(name=name, client_code=client_code)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def get_clients(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Client).order_by(models.Client.name).offset(skip).limit(limit).all()