from fastapi import FastAPI, HTTPException
from typing import Optional

app = FastAPI()

posts = [
    {"id": 1, "title": "News 1", "body": "Text 1"},
    {"id": 2, "title": "News 2", "body": "Text 2"},
    {"id": 3, "title": "News 3", "body": "Text 3"}
]


@app.get("/")
async def home():
    return [1, 2, 3, 5, 6, 7]

@app.get("/items")
async def items() -> list:
    return posts

@app.get("/items/{id}")
async def get_item(id: int) -> dict:
    for p in posts:
        if p["id"] == id:
            return p

    raise HTTPException(status_code=404, detail="Post not found")


@app.get("/search")
async def search(post_id: Optional[int] = None) -> dict:
    if post_id:
        for p in posts:
            if p["id"] == post_id:
                return p

        raise HTTPException(status_code=404, detail="Post not found")
    else:
        return {"data": "No post id provided"}
