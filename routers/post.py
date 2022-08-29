from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from database import get_db
import schemas, models, oauth2


router = APIRouter(
    prefix= "/posts",
    tags=['posts']
)

# @router.get("/", response_model=List[schemas.PostResponse])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), per_page: int = 10, page: int = 1, search: Optional[str] = ""):

    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(per_page).offset(per_page*(page-1)).all()


    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    post = models.Post(user_id=user.id, **post.dict() )

    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db)): 
    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id {id} was not found")

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if not post.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id {id} does not exist")
    print(post)
    if post.first().user_id != user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail = "Not authorized to perform requested action")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_post(id: int, body: schemas.PostCreate,  db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id {id} does not exist")

    if post.user_id != user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail = "Not authorized to perform requested action")

    post_query.update(body.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()

