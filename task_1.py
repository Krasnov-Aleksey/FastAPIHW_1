"""
Создать API для добавления нового пользователя в базу данных. Приложение
должно иметь возможность принимать POST запросы с данными нового
пользователя и сохранять их в базу данных.
Создайте модуль приложения и настройте сервер и маршрутизацию.
Создайте класс User с полями id, name, email и password.
Создайте список users для хранения пользователей.
Создайте маршрут для добавления нового пользователя (метод POST).
Реализуйте валидацию данных запроса и ответа.
Создайте маршрут для обновления информации о пользователе (метод PUT).
Создайте маршрут для удаления информации о пользователе (метод DELETE).
Реализуйте проверку наличия пользователя в списке и удаление его из
списка.
Создать веб-страницу для отображения списка пользователей. Приложение
должно использовать шаблонизатор Jinja для динамического формирования HTML
страницы.
Создайте HTML шаблон для отображения списка пользователей. Шаблон должен
содержать заголовок страницы, таблицу со списком пользователей и кнопку для
добавления нового пользователя.
Создайте маршрут для отображения списка пользователей (метод GET).
Реализуйте вывод списка пользователей через шаблонизатор Jinja.

"""

from fastapi import FastAPI, HTTPException, Request, Form
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class User(BaseModel):
    id: int
    name: str
    email: str
    password: str


user1 = User(id=1, name='user1', email='user1@m.ru', password='12341')
user2 = User(id=2, name='user2', email='user2@m.ru', password='12342')
user3 = User(id=3, name='user3', email='user3@m.ru', password='12343')

users = [user1, user2, user3]


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    context = {'users': users}
    return templates.TemplateResponse('base.html', {'request': request, 'name': 'Список пользователей', **context})


@app.post('/user/')
async def create_user(id=Form(), name=Form(), email=Form(), password=Form()):
    new_user = User(id=id, name=name, email=email, password=password)
    users.append(new_user)
    return f'Пользователь {new_user} добавлен'


@app.put('/user/{id_user}')
async def update_user(id_user: int, new_user: User):
    for i in range(len(users)):
        if users[i].id == id_user:
            users[i] = new_user
    return new_user


@app.delete('/user/{id_user}')
async def delete_user(id_user: int):
    for i in range(len(users)):
        if users[i].id == id_user:
            users.pop(i)
            return {'msg': 'Delete'}
    return HTTPException(status_code=404, detail='User not found')
