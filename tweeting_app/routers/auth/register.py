import sys
sys.path.append("../..")

from fastapi import APIRouter,Depends, Response,status
from pydantic import BaseModel,Field,EmailStr
from sqlalchemy.orm import Session
from datetime import datetime
from tweeting_app.database import models
from tweeting_app.database.database import engine,SessionLocal,get_db
from passlib.context import CryptContext

models.Base.metadata.create_all(bind=engine)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

router = APIRouter(tags=["Register New User"])

def encrypt_password(password):
    return bcrypt_context.hash(password)

class User(BaseModel):
    username: str = Field(min_length=5,max_length=30)
    email: EmailStr
    password: str = Field(min_length=3)
    is_active: bool
    is_superuser: bool

    class Config:
        schema_extra = {
            "example": {
                "username":"abhishek",
                "email":"abhishek@gmail.com",
                "password":"abc123",
                "is_active": False,
                "is_superuser": False
            }
        }

@router.post("/register/user",status_code=201)
async def register_new_user(user: User,response:Response,
                            db: Session = Depends(get_db)):
    new_user = models.User()

    username_lookup = db.query(models.User)\
            .filter(models.User.username == user.username)\
            .first()

    email_lookup = db.query(models.User)\
            .filter(models.User.email == user.email)\
            .first()

    if username_lookup is not None:
        response.status_code = status.HTTP_409_CONFLICT
        return {"Transaction":"Failure",
                "Reason": "Username Already Registered"}    

    if email_lookup is not None:
        response.status_code = status.HTTP_409_CONFLICT
        return {"Transaction":"Failure",
                "Reason": "Email Already Registered"}

    new_user.username = user.username
    new_user.email = user.email
    new_user.password = encrypt_password(user.password)
    new_user.is_active = user.is_active
    new_user.is_superuser = user.is_superuser
    new_user.time_created = datetime.utcnow()

    db.add(new_user)
    db.commit()

    return {"Transaction": "Success",
            "Reason": "User Registered Successfully"}