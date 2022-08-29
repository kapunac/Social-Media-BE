from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session

from database import get_db
import schemas, models, utils


router = APIRouter(
    prefix= "/users",
    tags=['users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(body: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(body.password)

    user = models.User(**body.dict())
    user.password = hashed_password
    #hash them passwords

    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

@router.get('/{id}', response_model= schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"User with id {id} couldn't be found")
    
    return user