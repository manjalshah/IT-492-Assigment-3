from sqlalchemy.orm import Session

import models
import schemas

def usered(db: Session, user_id: str):
    return db.query(models.steams).filter(models.steams.userid == user_id).all()

def userhr(db: Session, user_id: str):
    return db.query(models.steams.gamename,models.steams.gtype,models.steams.hrs).filter(models.steams.userid == user_id).all()

def create_user_item(db: Session, item: schemas.steamer):
    db_item = models.steams(userid = item.userid, gamename=item.gamename, gtype=item.gtype, hrs = item.hrs)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item