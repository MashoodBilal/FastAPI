from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlmodel import create_engine, SQLModel, Session
from typing import Annotated

engine = create_engine("sqlite:///todo.db")
# db = database
def create_db(): SQLModel.metadata.create_all(engine)

# lifespan will create database function
async def lifespan(app: FastAPI):
    create_db()
    yield

# will be use to update database from inside api
def update_session():
    with Session(engine) as session:
        yield session


# start of actual code of fastapi
# lifespan will run only once
app = FastAPI(lifespan=lifespan)

# class for todo. reduce rewriting of code in each method
class Todo(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

todo_list: list[Todo] = []

# Method to read all todos
@app.get("/")
async def read_all_todos():
    return todo_list

# Method to create a todo
@app.post("/create-todo")
async def create_todo(todo: Todo, session: Annotated[Session, Depends(update_session)]):
    todo.id = len(todo_list) + 1
    todo_list.append(todo)
    return todo

# Method to get/read/lookup a todo
@app.get("/get-todo/{id}")
async def get_todo(id: int, session: Annotated[Session, Depends(update_session)]):
    for todo in todo_list:
        if todo.id == id:
            return todo
    return {"error": "Todo not found"}

# Method to update a todo
@app.put("/update-todo/{id}")
async def update_todo(id: int, todo: Todo, session: Annotated[Session, Depends(update_session)]):
    for i, t in enumerate(todo_list):
        if t.id == id:
            todo_list[i] = todo
            return todo
    return {"error": "Todo not found"}

# Method to delete a todo
@app.delete("/delete-todo/{id}")
async def delete_todo(id: int, session: Annotated[Session, Depends(update_session)]):
    for i, todo in enumerate(todo_list):
        if todo.id == id:
            del todo_list[i]
            return {"message": "Todo deleted"}
    return {"error": " Todo not found"}