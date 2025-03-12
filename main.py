
from typing import Optional
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"Hello World"}


@app.get("/blog")
def index(limit: int = 10, published: bool = True, sort: Optional[str] = None):

    # only get 10 published blogs
    # return published
    if published:
        return {"data": f" {limit} published blogs from db"}
    else:
        return {"date": f"{limit} from the db"}


@app.get("/blog/unpublished")
def unpublished():
    return {"data": "all unpublished blogs"}


@app.get("/blog/{id}")
def show(id: int):
    return {"data": id}


@app.get("/blog/{id}/comments")
def comments(id, limit=10):
    # fetch comments of blog with the id :id

    return {"data": {"1", "2"}}


class Blog(BaseModel):
    title: str
    body: str
    published_at: Optional[bool]


@app.post("/blog")
def create_blog(blog: Blog):
    # return request
    return {"data": f"Blog is created  with title as {blog.title}"}


if __name__ == "__main__":
    uvicorn.run(app, debug=True, port=3000)
