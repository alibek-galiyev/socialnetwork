from fastapi import FastAPI, Response, status, HTTPException, Depends
from psycopg2 import connect, sql
from psycopg2.extras import RealDictCursor
from time import sleep
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


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


@app.get("/sqlalchemy/posts", response_model=list[schemas.PostResponse])
def get_posts_sqlalchemy(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.get("/posts", response_model=list[schemas.PostResponse])
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.CreatePost):
    cursor.execute("""
        INSERT INTO posts (title, content, published, rating)
        VALUES (%s, %s, %s, %s) returning *""", 
        (post.title, post.content, post.published, post.rating)
    )
    new_post = cursor.fetchone()
    conn.commit()
    return new_post


@app.post("/sqlalchemy/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts_sqlalchemy(post: schemas.CreatePost, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{post_id}", response_model=schemas.PostResponse)
def get_post(post_id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(post_id),))
    post = cursor.fetchone()
    if post:
        return post
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )
    

@app.get("/sqlalchemy/posts/{post_id}", response_model=schemas.PostResponse)
def get_post_sqlalchemy(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post:
        return post
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
    

@app.delete("/sqlalchemy/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_sqlalchemy(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post:
        db.delete(post)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )


@app.put("/posts/{post_id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def update_post(post_id: int, post: schemas.UpdatePost):
    cursor.execute("""
        UPDATE posts
        SET title = %s, content = %s, published = %s, rating = %s
        WHERE id = %s RETURNING *""",
        (post.title, post.content, post.published, post.rating, str(post_id))
    )
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post:
        return updated_post
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )
    

@app.put("/sqlalchemy/posts/{post_id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def update_post_sqlalchemy(post_id: int, post: schemas.UpdatePost, db: Session = Depends(get_db)):
    existing_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if existing_post:
        update_data = post.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                setattr(existing_post, key, value)
        db.commit()
        db.refresh(existing_post)
        return existing_post
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )
    

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user