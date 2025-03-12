from typing import List
from fastapi import FastAPI, Depends, Form, status, Response, HTTPException
from . import schema, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
import logging
from .hashing import Hash

app = FastAPI()
models.Base.metadata.create_all(engine)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=["blogs"])
def create(request: schema.Blog, db: Session = Depends(get_db)):
    # return {"title": request.title, "body": request.body}
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["blogs"])
def delete(id, db: Session = Depends(get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} not found",
        )

    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return "done"


@app.get("/blog/{id}", status_code=200, response_model=schema.ShowBlog, tags=["blogs"])
def show(id: int, db: Session = Depends(get_db)):
    # logger.info(f"Received request for blog with id: {id}")
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} is not available",
        )
    return blog


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["blogs"])
def update(id: int, request: schema.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} not found",
        )

    # Convert the Pydantic model to a dictionary and exclude unset fields
    blog_data = request.model_dump(exclude_unset=True)
    db.query(models.Blog).filter(models.Blog.id == id).update(blog_data)
    db.commit()
    db.refresh()

    return {"message": "Updated successfully"}


@app.get("/blog", response_model=List[schema.ShowBlog], tags=["blogs"])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.post("/user", response_model=schema.ShowUser, tags=["user"])
def create_user(request: schema.User, db: Session = Depends(get_db)):
    user = request.model_dump(exclude_unset=True)
    hashed_password = Hash.bcrypt(user["password"])
    user["password"] = hashed_password
    # logger.info(f"Find what is the user hold {user} ")
    # logger.info(f"Creating user with data: {user.exclude_keys('password')}")
    new_user = models.User(**user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/user/{id}", response_model=schema.ShowUser, tags=["user"])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {id} not found",
        )
    return user
