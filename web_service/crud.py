from sqlalchemy.orm import Session

import models
import schemas

def usered(db: Session, user_id: str):
    return db.query(models.steams).filter(models.steams.userid == user_id).all()

def userhr(db: Session, user_id: str):
    return db.query(models.steams.gamename,models.steams.gtype,models.steams.hrs).filter(models.steams.userid == user_id).all()


# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()
#m
#
# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()
#
#
# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()
#`
#
# def create_user(db: Session, user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(
#         email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
#
#
# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()
#
#
def create_user_item(db: Session, item: schemas.steamer):
    db_item = models.steams(userid = item.userid,gamename=item.gamename,gtype=item.gtype,hrs = item.hrs)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
