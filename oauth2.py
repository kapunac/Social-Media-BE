from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import schemas, database, models
from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# secret key
# Algorithm
# expiration time
# openssl rand  -hex 32 -> get random string of 32 chars

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)

    return encoded

def verify_access_token(token: str, credentials_exception):
    try: 
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        id: str = decoded_token.get("user_id")

        if not id:
            raise credentials_exception
        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
