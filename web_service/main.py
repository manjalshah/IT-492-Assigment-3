from fastapi import Depends, FastAPI, HTTPException, Request, Form
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse,RedirectResponse
from database import SessionLocal, engine
import crud,models,schemas
from fastapi.templating import Jinja2Templates
from rec import reco
from mat_fact import recommend
from mat_fact import updater,LTR
import pandas as pd

templates = Jinja2Templates(directory="templates")
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/",response_class=HTMLResponse)
def homer(request: Request):
    return templates.TemplateResponse("hello.html",{"request":request})

@app.get("/upd",response_class=HTMLResponse)
def upder(request: Request):
    updater()
    return templates.TemplateResponse("hello.html", {"request": request})

@app.post("/process",response_class=HTMLResponse)
def tempo(*,ide:str = Form(...),request:Request):

    recommenda = recommend(ide)
    recommendations = reco(ide)

    print(recommendations)
    return templates.TemplateResponse("temprec.html", {"request":request,"recommendations": recommendations,"another":recommenda,"username":ide})

@app.get("/fina/{user}",response_class=HTMLResponse)
def tempo(user:str,request:Request):
    lis = LTR(user)
    return templates.TemplateResponse("recom.html", {"request":request,"recommendations": lis})

@app.get("/adder", response_class=HTMLResponse)
def adr(request:Request):
    return templates.TemplateResponse("adddd.html", {"request":request})


@app.post("/addata", response_class=HTMLResponse)
def create_item_for_user(*,request:Request,userid : str= Form(),gamename : str= Form(),gtype : str= Form(),hrs : int = Form(),db: Session = Depends(get_db)):
    print("hello moto")
    new_user = schemas.steamer(userid=userid,gamename=gamename,gtype=gtype,hrs=hrs)

    crud.create_user_item(db=db, item=new_user)
    return templates.TemplateResponse("hello.html",{"request":request})