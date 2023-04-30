from pydantic import BaseModel


class steamer(BaseModel):
    userid: str
    gamename: str
    gtype: str
    hrs : int
    class Config:
        orm_mode = True

class steamhr(BaseModel):
    # userid: str
    gamename: str
    gtype: str
    hrs : int
    class Config:
        orm_mode = True

