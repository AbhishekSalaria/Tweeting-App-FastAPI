import sys
sys.path.append("..")

from fastapi import APIRouter,Depends,Response,status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
from tweeting_app.database.database import engine,SessionLocal,get_db
from tweeting_app.routers.auth.login import get_current_user
from tweeting_app.database import models

models.Base.metadata.create_all(bind=engine)

router = APIRouter(tags=["Superuser API"])

def check_superuser(db,user):
    user_model = db.query(models.User).filter(models.User.id == user.get("user_id")).first()

    if user_model.is_superuser == False:
        return False
    return True 

@router.get("/tweets/get/all/users",status_code=200)
async def get_all_tweets_of_all_users(response: Response,
                        db:Session = Depends(get_db),
                        user:dict = Depends(get_current_user)):
    if(check_superuser(db,user) == False):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"Transaction": "Failure",
                "Reason": "Not A superuser"}
    
    return db.query(models.Tweet).all()

@router.get("/tweets/get/all/user/{user_id}")
async def get_all_tweets_of_single_user(user_id: int,
                                        response:Response,
                                        db:Session = Depends(get_db),
                                        user:dict = Depends(get_current_user)):
    
    if(check_superuser(db,user) == False):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"Transaction": "Failure",
                "Reason": "Not A superuser"}
    
    return db.query(models.Tweet).filter(models.Tweet.user_id == user_id).all()

@router.get("/get/all/users")
async def get_all_users(response: Response,
                        db:Session = Depends(get_db),
                        user:dict = Depends(get_current_user)):
    
    if(check_superuser(db,user) == False):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"Transaction": "Failure",
                "Reason": "Not A superuser"}
    
    return db.query(models.User).all()

@router.get("/get/active/users")
async def get_active_users(response:Response,
                           db:Session = Depends(get_db),
                           user:dict = Depends(get_current_user)):
    
    if(check_superuser(db,user) == False):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"Transaction": "Failure",
                "Reason": "Not A superuser"}
    
    return db.query(models.User).filter(models.User.is_active == True).all()

@router.get("/get/inactive/users")
async def get_inactive_users(response:Response,
                             db:Session = Depends(get_db),
                             user:dict = Depends(get_current_user)):
    
    if(check_superuser(db,user) == False):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"Transaction": "Failure",
                "Reason": "Not A superuser"}
    
    return db.query(models.User).filter(models.User.is_active == False).all()

@router.delete("/tweet/delete/users/{tweet_id}")
async def delete_any_tweet(tweet_id: int,
                           response: Response,
                           db: Session = Depends(get_db),
                           user:dict = Depends(get_current_user)):
    
    if(check_superuser(db,user) == False):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"Transaction": "Failure",
                "Reason": "Not A superuser"}
    
    tweet_model = db.query(models.Tweet).filter(models.Tweet.id == tweet_id).first()

    if tweet_model is None:
         response.status_code = status.HTTP_404_NOT_FOUND
         return {"Transaction": "Failure",
                "Reason": "Invalid Tweet id"}

    db.query(models.Tweet).filter(models.Tweet.id == tweet_id).delete()
    db.commit()

    return {"Transaction": "Success",
            "Reason": "Tweet Deleted Successfully"}

@router.delete("/account/delete/user/{user_id}")
async def delete_user(user_id: int,
                      response: Response,
                      db: Session = Depends(get_db),
                      user:dict = Depends(get_current_user)):
    
    if(check_superuser(db,user) == False):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"Transaction": "Failure",
                "Reason": "Not A superuser"}
    
    db.query(models.User).filter(models.User.id == user_id).delete()
    db.query(models.Tweet).filter(models.Tweet.user_id == user_id).delete()
    db.commit()

    return {"Transaction": "Success",
            "Reason": "User Deleted Successfully"}

@router.put("/account/active/user/{user_id}")
async def make_user_active(user_id: int,
                           response: Response,
                           db: Session = Depends(get_db),
                           user:dict = Depends(get_current_user)):
    
    if(check_superuser(db,user) == False):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"Transaction": "Failure",
                "Reason": "Not A superuser"}
    
    user_model = db.query(models.User).filter(models.User.id == user_id).first()
    user_model.is_active = True

    db.add(user_model)
    db.commit()

    return {"Transaction": "Success",
            "Reason": "User is Now Active"}

@router.put("/account/inactive/user/{user_id}")
async def make_user_inactive(user_id: int,
                             response:Response,
                             db: Session = Depends(get_db),
                             user:dict = Depends(get_current_user)):
    
    if(check_superuser(db,user) == False):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"Transaction": "Failure",
                "Reason": "Not A superuser"}
    
    user_model = db.query(models.User).filter(models.User.id == user_id).first()
    user_model.is_active = False

    db.add(user_model)
    db.commit()

    return {"Transaction": "Success",
            "Reason": "User is Now In-Active"}