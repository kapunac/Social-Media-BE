from curses.ascii import HT
from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import schemas, models, oauth2

router = APIRouter(
    prefix= "/votes",
    tags=['Post voting']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user) ):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} couldn't be found")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == user.id)
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {user.id} has already voted on the post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")

        vote_query.delete(synchronize_session= False)
        db.commit()
        return {"Message": "Successfully removed vote"}

