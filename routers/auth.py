from os import access
from fastapi import status, HTTPException, Response, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
import schemas, models, utils, oauth2

router = APIRouter(
    tags=['Authentication']
)


@router.post('/login', response_model= schemas.Token)
def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    if not utils.verify(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    # create token
    # return token

    access_token = oauth2.create_access_token(data= {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}