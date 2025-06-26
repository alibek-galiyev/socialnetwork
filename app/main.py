from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel
from psycopg2 import connect, sql
from psycopg2.extras import RealDictCursor
from time import sleep
from . import models
from .database import engine, get_db
from datetime import datetime
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


class Post(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    published: bool = True
    created_at: Optional[datetime] = None
    rating: Optional[int] = None


# my_posts = [
#     {"id": 1, "title": "Post 1", "content": "Content of post 1", "published": True},
#     {"id": 2, "title": "Post 2", "content": "Content of post 2", "published": False},
# ]

while True:
    try:
        conn = connect(
            host="localhost",
            database="socialnetwork",
            user="alibek",
            password="1653",
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection successful")
        break
    except Exception as e:
        print("Database connection failed")
        print(f"Error: {e}")
        sleep(2)





@app.get("/")
def root():
    return {"message": "Welcome to my API!"}


@app.get("/sqlalchemy/posts")
def get_posts_sqlalchemy(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""
        INSERT INTO posts (title, content, published, rating)
        VALUES (%s, %s, %s, %s) returning *""", 
        (post.title, post.content, post.published, post.rating)
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(post_id),))
    post = cursor.fetchone()
    if post:
        return {"data": post}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(post_id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )


@app.put("/posts/{post_id}", status_code=status.HTTP_200_OK)
def update_post(post_id: int, post: Post):
    cursor.execute("""
        UPDATE posts
        SET title = %s, content = %s, published = %s, rating = %s
        WHERE id = %s RETURNING *""",
        (post.title, post.content, post.published, post.rating, str(post_id))
    )
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post:
        return {"data": updated_post}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )