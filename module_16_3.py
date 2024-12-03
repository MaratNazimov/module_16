from fastapi import FastAPI, Path
from typing import Annotated
from fastapi import HTTPException


app = FastAPI()

users = [
    {"id": 1, "Имя": "Example", "возраст": 18}
]

@app.get("/users")
async def get_users():
    return users


@app.post("/user/{username}/{age}")
async def create_user(
        username: Annotated[str, Path(min_length=3,
                                      max_length=20,
                                      description="Enter username",
                                      example="Human")],
        age: Annotated[int, Path(gt=17,
                                 le=100,
                                 description="Enter age",
                                 example=18)])\
        -> str:
    user_id = max(user["id"] for user in users) + 1
    new_user = {"id": user_id, "Имя": username, "возраст": age}
    users.append(new_user)
    return f"User {user_id} is registered"


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(
        user_id: Annotated[int, Path(le=1000,
                                     description="Enter id")],
        username: Annotated[str, Path(min_length=3,
                                      max_length=20,
                                      description="Enter username",
                                      example="Human")],
        age: Annotated[int, Path(gt=17,
                                 le=100,
                                 description="Enter age",
                                 example=18)])\
        -> str:
    for user in users:
        if user["id"] == user_id:
            user["Имя"] = username
            user["возраст"] = age
            return f"The user {user_id} is updated"
    raise HTTPException(status_code=404, detail="id не найден")


@app.delete("/user/{user_id}")
async def delete_user(
        user_id: Annotated[int, Path(le=1000,
                                     description="Enter id")])\
        -> str:
    for i, user in enumerate(users):
        if user["id"] == user_id:
            del users[i]
            return f"User {user_id} delete"
    raise HTTPException(status_code=404, detail="id не найден")
