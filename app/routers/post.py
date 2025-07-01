from fastapi import status, HTTPException, Depends, APIRouter, Response
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import Optional


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=list[schemas.PostResponse])
def get_posts_sqlalchemy(
    db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""
    ):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return posts


# @router.get("/posts", response_model=list[schemas.PostResponse])
# def get_posts():
#     cursor.execute("""SELECT * FROM posts""")
#     posts = cursor.fetchall()
#     return posts


# @router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
# def create_posts(post: schemas.CreatePost):
#     cursor.execute("""
#         INSERT INTO posts (title, content, published, rating)
#         VALUES (%s, %s, %s, %s) returning *""", 
#         (post.title, post.content, post.published, post.rating)
#     )
#     new_post = cursor.fetchone()
#     conn.commit()
#     return new_post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts_sqlalchemy(
    post: schemas.CreatePost, 
    db: Session = Depends(get_db), 
    get_current_user: int = Depends(oauth2.get_current_user)
    ):

    new_post = models.Post(owner_id=get_current_user.id, **post.model_dump(exclude={"owner_id"}))
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# @router.get("/posts/{post_id}", response_model=schemas.PostResponse)
# def get_post(post_id: int):
#     cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(post_id),))
#     post = cursor.fetchone()
#     if post:
#         return post
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post with id {post_id} not found"
#         )
    

@router.get("/{post_id}", response_model=schemas.PostResponse)
def get_post_sqlalchemy(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post:
        return post
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )


# @router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(post_id: int):
#     cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(post_id),))
#     deleted_post = cursor.fetchone()
#     conn.commit()
#     if deleted_post:
#         return Response(status_code=status.HTTP_204_NO_CONTENT)
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post with id {post_id} not found"
#         )
    

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_sqlalchemy(post_id: int, db: Session = Depends(get_db),
                           get_current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post:
        if post.owner_id != get_current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this post"
            )
        db.delete(post)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )


# @router.put("/posts/{post_id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
# def update_post(post_id: int, post: schemas.UpdatePost):
#     cursor.execute("""
#         UPDATE posts
#         SET title = %s, content = %s, published = %s, rating = %s
#         WHERE id = %s RETURNING *""",
#         (post.title, post.content, post.published, post.rating, str(post_id))
#     )
#     updated_post = cursor.fetchone()
#     conn.commit()
#     if updated_post:
#         return updated_post
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post with id {post_id} not found"
#         )
    

@router.put("/{post_id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def update_post_sqlalchemy(
    post_id: int, 
    post: schemas.UpdatePost, 
    db: Session = Depends(get_db),
    get_current_user: int = Depends(oauth2.get_current_user)
    ):
    existing_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if existing_post:
        if existing_post.owner_id != get_current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this post"
            )
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