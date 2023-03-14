import sys
sys.path.append("..")

from fastapi import FastAPI
from tweeting_app.database.database import engine,SessionLocal
from tweeting_app.database import models
from tweeting_app.routers import tweetapi,superuserapi
from tweeting_app.routers.auth import login, register

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(register.router)
app.include_router(login.router)
app.include_router(tweetapi.router)
app.include_router(superuserapi.router)