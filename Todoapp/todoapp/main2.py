from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

app = FastAPI()

engine = create_engine('sqlite:///todo.db')
Base = declarative_base()

class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)

@app.get("/todos/")
async def read_todos():
    connection = engine.connect()
    result = connection.execute("SELECT * FROM todos")
    todos = [dict(row) for row in result.fetchall()]
    return JSONResponse(content={"todos": todos}, media_type="application/json")

class CreateTodo(BaseModel):
    title: str
    description: str

@app.post("/todos/")
async def create_todo(todo: CreateTodo):
    new_todo = Todo(title=todo.title, description=todo.description)
    Base.metadata.create_all(engine)
    app.db.execute("INSERT INTO todos (title, description) VALUES (:title, :description)", 
                    {'title': todo.title, 'description': todo.description})
    return JSONResponse(content={"message": "Todo created successfully"}, media_type="application/json")
