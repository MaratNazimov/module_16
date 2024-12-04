from fastapi import FastAPI, status, Body, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import List
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="templates")
users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int


class UserCreate(BaseModel):
    username: str = Field(...,
                          min_length=3,
                          max_length=20,
                          description="Enter username")
    age: int = Field(gt=17,
                     le=100,
                     description="Enter age",)


@app.get("/")
def get_all_users(request: Request) -> HTTPException:
    return templates.TemplateResponse()

@app.get(path="/user/{user_id}")
async def get_user(user_id: int) -> User:
    try:
        return users[user_id - 1]
    except:
        raise HTTPException(status_code=404, detail="User was not found")


@app.post("/user/{username}/{age}")
async def create_user(user: UserCreate) -> User:
    user_id = max((user.id for user in users), default=0) + 1
    new_user = User(id = user_id, username = user.username, age = user.age)
    users.append(new_user)
    return new_user


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: int, user: UserCreate) -> User:
    for i in users:
        if i.id == user_id:
            i.username = user.username
            i.age = user.age
            return user
    raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}")
async def delete_user(user_id: int) -> str:
    for i, j in enumerate(users):
        if j.id == user_id:
            del users[i]
            return f"User {user_id} delete"
    raise HTTPException(status_code=404, detail="User was not found")