from fastapi import FastAPI, HTTPException, Path, Query, Body
from typing import Optional, List, Dict, Annotated
from pydantic import BaseModel, Field

app = FastAPI()


class User(BaseModel):
    id: int
    username: str
    email: str


class UserCreate(BaseModel):
    username: Annotated[
        str,
        Field(title="Username", min_length=2, max_length=20)
    ]
    email: Annotated[
        str,
        Field(title="Email", min_length=10, max_length=30)
    ]


users = [
    {
        "id": 1,
        "username": "Azamat01",
        "email": "aza@gmail.com"
    },
    {
        "id": 2,
        "username": "Marat03",
        "email": "mara@mail.com"
    },
    {
        "id": 3,
        "username": "Kuba27",
        "email": "kuba@gmail.com"
    }
]


@app.get("/users")
async def get_users() -> List[User]:
    return [User(**user) for user in users]


@app.get("/users/{id}")
async def get_user(id: Annotated[int, Path(..., title="Здесь указываеться ID пользователя", ge=1, lt=100)]) -> User:
    for user in users:
        if user["id"] == id:
            return User(**user)
    raise HTTPException(status_code=404, detail="User not found")


@app.post("/user/add")
async def add_user(user: Annotated[
    UserCreate,
    Body(..., example={
        "username": "Username",
        "email": "user@example.com"
    })
]) -> User:
    new_user_id = len(users) + 1
    new_user = {
        "id": new_user_id,
        "username": user.username,
        "email": user.email
    }
    users.append(new_user)
    return User(**new_user)

@app.delete("/user/delete/{id}")
async def delete_user(id: int) -> Dict:
    for user in users:
        if user["id"] == id:
            users.remove(user)
            return {"message": "User was deleted"}
    raise HTTPException(status_code=404, detail="User not found")


@app.get("/search")
async def search(user_id: Annotated[
    Optional[int],
    Query(title="ID of user to search for", ge=1, lt=100)
]) -> Dict[str, Optional[User]]:
    if user_id:
        for book in users:
            if book["id"] == user_id:
                return {"data": User(**book)}
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return {"data": None}


