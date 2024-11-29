from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def main_page():
    return "Главная страница"

@app.get("/user/admin")
async def user_admin():
    return "Вы вошли как администратор"

@app.get("/user/{user_id}")
async def users_id(user_id = int):
    return f"Вы вошли как пользователь № {user_id}"

@app.get("/user/{username}/{age}")
async def users(username = str, age = int):
    return f"Информация о пользователе. Имя: {username}, Возраст: {age}"
