from fastapi import FastAPI, Response, status, HTTPException, Depends
from psycopg2 import connect, sql
from psycopg2.extras import RealDictCursor
from time import sleep
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import post, user, auth


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Welcome to my API!"}

