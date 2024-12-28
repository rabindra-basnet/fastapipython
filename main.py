import uvicorn
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def index():
    return {"data": {"name": "Rabindra"}}


@app.get("/about")
def index():
    return {"data": "about page"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000, reload=True)
