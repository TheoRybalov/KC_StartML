from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional
from database import SessionLocal
from table_post import Post
from table_user import User
from table_feed import Feed
from schema import UserGet, PostGet, FeedGet

app = FastAPI()



def get_db():
    with SessionLocal() as db:
        return db
    

@app.get("/user/{id}", response_model = UserGet)
def user_into(id: int, db: Session = Depends(get_db)):
    result =  db.query(User).filter(User.id == id).first()
    if not result:
        raise HTTPException(404, "user not found")
    else:
        return result
    

@app.get("/post/{id}", response_model = PostGet)
def post_into(id: int, db: Session = Depends(get_db)):
    result =  db.query(Post).filter(Post.id == id).first()
    if not result:
        raise HTTPException(404, "user not found")
    else:
        return result

@app.get("/user/{id}/feed", response_model = List[FeedGet])
def user_feed_into(id: int, limit: int = 10,  db: Session = Depends(get_db)):
    result =  (
        db.query(Feed)
        .filter(Feed.user_id == id)
        .order_by(Feed.time.desc())
        .limit(limit)
        .all()
    )
    return result

@app.get("/post/{id}/feed", response_model = List[FeedGet])
def post_feed_into(id: int, limit: int = 10,  db: Session = Depends(get_db)):
    result =  (
        db.query(Feed)
        .filter(Feed.post_id == id)
        .order_by(Feed.time.desc())
        .limit(limit)
        .all()
    )
    return result

@app.get("/post/recommendations/", response_model = List[PostGet])
def get_recommended_feed(id: Optional[int] = None, limit: int = 10,  db: Session = Depends(get_db)):
    result =  (
        db.query(Post)
        .select_from(Feed)
        .filter(Feed.action == "like")
        .join(Post, Post.id == Feed.post_id)
        .group_by(Post.id)
        .order_by(desc(func.count(Feed.post_id)))
        .limit(limit)
        .all()
    )
    return result
    

