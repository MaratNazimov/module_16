from fastapi import FastAPI, HTTPException, Request, Path
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Annotated
from fastapi.templating import Jinja2Templates


app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True}, debug=True)
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


@app.get("/", response_class=HTMLResponse)
def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get(path="/user/{user_id}", response_class=HTMLResponse)
async def get_user(request: Request, user_id: Annotated[int, Path(ge=1)]) -> HTMLResponse:
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse("users.html", {"request": request, "user": user})
    raise HTTPException(status_code=404, detail="User was not found")


@app.post("/user/{username}/{age}", response_class=HTMLResponse)
async def create_user(request: Request, user: UserCreate) -> HTMLResponse:
    user_id = max((user.id for user in users), default=0) + 1
    new_user = User(id = user_id, username = user.username, age = user.age)
    users.append(new_user)
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.put("/user/{user_id}/{username}/{age}", response_class=HTMLResponse)
async def update_user(request: Request, user_id: Annotated[int, Path(ge=1)], user: UserCreate) -> HTMLResponse:
    for i in users:
        if i.id == user_id:
            i.username = user.username
            i.age = user.age
            return templates.TemplateResponse("users.html", {"request": request, "users": users})
    raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}", response_class=HTMLResponse)
async def delete_user(request: Request, user_id: Annotated[int, Path(ge=1)]) -> HTMLResponse:
    for i, j in enumerate(users):
        if j.id == user_id:
            del users[i]
            return templates.TemplateResponse("users.html", {"request": request, "users": users})
    raise HTTPException(status_code=404, detail="User was not found")