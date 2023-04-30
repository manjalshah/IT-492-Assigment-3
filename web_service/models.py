from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from database import Base


class steams(Base):
    __tablename__ = "steams"

    userid = Column(String)
    gamename = Column(String)
    gtype = Column(String)
    hrs = Column(Integer)
    __table_args__ = (
        PrimaryKeyConstraint(userid, gamename,gtype,hrs),
        {},
    )



