from symtable import Class

from fastapi import FastAPI, HTTPException
from typing import Optional, List, Dict
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    id: int
    username: str
    email: str


class UserCreate(BaseModel):
    username: str
    email: str


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
async def get_user(id: int) -> User:
    for user in users:
        if user["id"] == id:
            return User(**user)
    raise HTTPException(status_code=404, detail="User not found")


@app.post("/user/add")
async def add_user(user: UserCreate) -> User:
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


