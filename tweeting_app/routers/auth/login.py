import sys
sys.path.append("../..")

from fastapi import APIRouter,Depends, HTTPException,status,Response,status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from tweeting_app.database.database import engine,SessionLocal,get_db
from passlib.context import CryptContext
from tweeting_app.database import models
from typing import Optional
from jose import jwt,JWSError

SECRET_KEY = "This_is_a_top_secret_key_to_be_used_for_jwt"
ALGORITHM = "HS256"

models.Base.metadata.create_all(bind=engine)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(tags=["Login User For Access Token"])

def verify_password(plain_password, encrypted_password):
    return bcrypt_context.verify(plain_password,encrypted_password)

def authenticate_user(username:str, password: str, db):
    user_model = db.query(models.User)\
        .filter(models.User.username == username).first()
    
    if user_model is None:
        return False
    
    if verify_password(password,user_model.password) == False:
        return False
    
    return user_model

def get_access_token(username:str,user_id:int,
                     expire_time: Optional[timedelta] = None):
    if expire_time:
        expire = datetime.utcnow() + expire_time
    else:
        expire = datetime.utcnow() + timedelta(minutes=20)
    
    encode = {"sub":username,"id":user_id,"exp":expire}

    return jwt.encode(encode, SECRET_KEY,ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id:int = payload.get("id")
        if username is None or user_id is None:
            return unsuccessful_token_response()
        return {"username":username,"user_id":user_id}
    except JWSError:
        return unsuccessful_token_response()

@router.post("/login/user",status_code=200)
async def login_user(response: Response,
                     user: OAuth2PasswordRequestForm = Depends(),
                     db: Session = Depends(get_db)):

    user_model = authenticate_user(user.username,user.password, db)

    if not user_model:
        response.status_code = status.HTTP_404_NOT_FOUND
        return login_exception()
    
    token_expire = timedelta(minutes=30)

    token = get_access_token(user_model.username,user_model.id, token_expire)

    return {
        "Transaction": "Success",
        "Credentials":{
            "Access Token": token,
            "Type": "bearer"}
    }

def login_exception():
    login_exception_response = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect Username or Password",
        headers={"WWW-Authenticate": "Bearer"}
    )
    return login_exception_response

def unsuccessful_token_response():
    return {"Transaction": "Failure",
            "Reason":"Token Modified"}    