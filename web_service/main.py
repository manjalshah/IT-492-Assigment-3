from fastapi import Depends, FastAPI, HTTPException, Request, Form
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse,RedirectResponse
from database import SessionLocal, engine
import crud,models,schemas
from fastapi.templating import Jinja2Templates
from rec import reco
from prep import prep
templates = Jinja2Templates(directory="templates")
from prep import FINAL_usergamemat,FINAL_simmat,FINAL_meanmapper
models.Base.metadata.create_all(bind=engine)
from mat_fact import recommend
from mat_fact import updater,LTR
import pandas as pd
app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @app.get("/users", response_model=schemas.steamer)
# def create_user(user: schemas.steamer, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)

# @app.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users
#
#
@app.get("/",response_class=HTMLResponse)
def homer(request: Request):
    return templates.TemplateResponse("hello.html",{"request":request})

# @app.get("/findfull/{user_id}", response_model=list[schemas.steamer])
# def read_user(user_id: str, db: Session = Depends(get_db)):
#     db_user = crud.usered(db, user_id=user_id)
#     print(db_user)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user
# @app.get("/findgames/{user_id}", response_model=list[schemas.steamhr])
# def read_user_hr(user_id: str, db: Session = Depends(get_db)):
#     db_user = crud.userhr(db, user_id=user_id)
#     print(db_user)\
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user

@app.get("/upd",response_class=HTMLResponse)
def upder(request: Request):
    prep()
    updater()
    return templates.TemplateResponse("hello.html", {"request": request})


#
#
# @app.put("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, user: schemas.User, skip: int, limit: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user flaqx  is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user
#
#
@app.post("/process",response_class=HTMLResponse)
def tempo(*,ide:str = Form(...),request:Request):

    recommenda = recommend(ide)
    recommendations = reco(FINAL_usergamemat,FINAL_simmat,FINAL_meanmapper,ide)

      # HTTPException(status_code=404, detail="User not found")
    print(recommendations)
    return templates.TemplateResponse("temprec.html", {"request":request,"recommendations": recommendations,"another":recommenda,"username":ide})

@app.get("/fina/{user}",response_class=HTMLResponse)
def tempo(user:str,request:Request):
    lis = LTR(user)
    return templates.TemplateResponse("recom.html", {"request":request,"recommendations": lis})


# @app.post("/anoprocess",response_class=HTMLResponse)
# def tempo(*,ide:str = Form(...),request:Request):
#     try:
#
#     except:
#         raise HTTPException(status_code=404, detail="User not found")
#     print(recommendations)
#     return templates.TemplateResponse("recom.html", {"request":request,"recommendations": recommendations})


@app.get("/adder", response_class=HTMLResponse)
def adr(request:Request):
    # gg = pd.read_sql(db.query(models.steams.gamename).statement, db.bind)
    # uniq = gg['gamename'].unique()
    return templates.TemplateResponse("adddd.html", {"request":request})


@app.post("/addata", response_class=HTMLResponse)
def create_item_for_user(*,request:Request,userid : str= Form(),gamename : str= Form(),gtype : str= Form(),hrs : int = Form(),db: Session = Depends(get_db)):
    print("hello moto")
    new_user = schemas.steamer(userid=userid,gamename=gamename,gtype=gtype,hrs=hrs)

    crud.create_user_item(db=db, item=new_user)
    return templates.TemplateResponse("hello.html",{"request":request})
#
#
# @app.get("/items/", response_model=list[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items
