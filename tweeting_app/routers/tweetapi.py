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

router = APIRouter(tags=["Tweet API"])

class Tweet(BaseModel):
    tweet: str

def check_active_user(db, user):
    
    user_model = db.query(models.User).filter(models.User.id == user.get("user_id")).first()

    if user_model.is_active:
        return True
    
    return False

@router.get("/tweet/get/user")
async def get_all_tweets(response: Response,
                         db:Session = Depends(get_db),
                         user:dict = Depends(get_current_user)):
    
    if(check_active_user(db,user) == False):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
                "Transaction":"Failure",
                "Reason":"Not an Active User",
                "Solution":"Contact Superuser to Change your status to active one."
        }
    
    user_tweets = db.query(models.Tweet).filter(models.Tweet.user_id == user.get("user_id")).all()

    if user_tweets is None:
        return {"Transaction":"Failure",
                "Reason":"No Tweets"}
    return user_tweets

@router.post("/tweet/post/user",status_code=200)
async def post_new_tweet(data:Tweet,
                         response:Response,
                         db:Session = Depends(get_db),
                         user:dict = Depends(get_current_user)):
    
    if(check_active_user(db,user) == False):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
                "Transaction":"Failure",
                "Reason":"Not an Active User",
                "Solution":"Contact Superuser to Change your status to active one."
        }
    
    tweet_model = models.Tweet()

    tweet_model.data = data.tweet
    time_created = datetime.utcnow()
    tweet_model.time_created = time_created
    tweet_model.last_modified = time_created
    tweet_model.user_id = user.get("user_id")

    db.add(tweet_model)
    db.commit()

    return {"Transaction":"Success",
            "Reason":"Tweet Published"}

@router.put("/tweet/edit/user/{tweet_id}",status_code=200)
async def edit_tweet(data:Tweet,
                     tweet_id: int,
                     response: Response,
                     db:Session = Depends(get_db),
                     user:dict = Depends(get_current_user)):

    if(check_active_user(db,user) == False):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
                "Transaction":"Failure",
                "Reason":"Not an Active User",
                "Solution":"Contact Superuser to Change your status to active one."
        }
    
    tweet_model = db.query(models.Tweet).filter(models.Tweet.id == tweet_id)\
                    .filter(models.Tweet.user_id == user.get("user_id")).first()

    if tweet_model is None:
        return {"Transaction":"Failure",
                "Reason":"No such Tweet"}

    tweet_model.data = data.tweet
    tweet_model.last_modified = datetime.utcnow()

    db.add(tweet_model)
    db.commit()

    return {"Transaction":"Success",
            "Reason":"Tweet Successfully Updated"}

@router.delete("/tweet/delete/user/{tweet_id}",status_code=200)
async def delete_user_tweet(tweet_id: int,
                            response: Response,
                            db:Session = Depends(get_db),
                            user:dict = Depends(get_current_user)):

    if(check_active_user(db,user) == False):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
                "Transaction":"Failure",
                "Reason":"Not an Active User",
                "Solution":"Contact Superuser to Change your status to active one."
        }

    user_tweet = db.query(models.Tweet).filter(models.Tweet.user_id == user.get("user_id"))\
        .filter(models.Tweet.id == tweet_id)\
        .first()

    if user_tweet is None:
        return {"Transaction":"Failure",
                "Reason":"No such Tweet"}
    
    db.query(models.Tweet).filter(models.Tweet.user_id == user.get("user_id"))\
        .filter(models.Tweet.id == tweet_id)\
        .delete()    
    
    db.commit()

    return {
        "Transaction":"Success",
        "Reason":"Tweet Deleted Successfully"
        }