from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from sqlmodel import Field, Session, SQLModel, create_engine
from sqlalchemy import (Boolean, Column, ForeignKey, Integer, String, Date)
from typing import List


class Todo(SQLModel, table=True):
    content: str = Field(index=True)

class Projects(Todo):
        __tablename__ = 'projects'

        id = Column(Integer, primary_key=True, index=True)
        name = Column(String)


class Tasks(Todo):
        __tablename__ = 'tasks'

        id = Column(Integer, primary_key=True, index=True)
        project = Column(String, ForeignKey("projects.id"))
        name = Column(String)
        date = Column(Date)
        priority = Column(Boolean)
        completed = Column(Boolean)

        def __repr__(self):
            return f"Tasks('{self.name}', '{self.date}')"

connection_string = str(
    "postgresql://postgres:password@localhost:5432/todoapp"
).replace(
    "postgresql", "postgresql+psycopg"
)

engine = create_engine(connection_string, connect_args={}, pool_recycle=300)

SQLModel.metadata.create_all(engine)



def get_db():
        try:
            db = Session(engine)
            yield db
        finally:
            db.close()

app = FastAPI()

@app.on_event("shutdown")
async def shutdown_db():
    await engine.dispose()

    #GET /projects (list):
    @app.get("/projects", response_model=List[Projects])
    def list_projects(db: Session = Depends(get_db)):
        return db.query(Projects).all()

    #POST /projects (create):
    @app.post("/projects", status_code=status.HTTP_201_CREATED)
    def create_project(data: Projects, db: Session = Depends(get_db)):
        project = db.query(Projects).filter(Projects.name == data.name)
        if project.first() is None:
            db.add(data)
            db.commit()
            return "Project Created"
        else:
            return "Project already exists"

#### GET/POST tasks:
    #GET /tasks (list):
    @app.get("/tasks", response_model=List[Tasks])
    def list_tasks(db: Session = Depends(get_db)):
        return db.query(Tasks).all()

    #POST /tasks (create):
    @app.post("/tasks")
    def create_task(data: Tasks, db: Session = Depends(get_db)):
        project = db.query(Projects).filter(Projects.name == data.project)
        if project.first() is None:
            return "Project does not exist"
        else:
            db.add(data)
            db.commit()
            return "Task Created"

#### GET/PUT/DELETE tasks:
    #GET /tasks (list):
    @app.get("/tasks/{name}")
    def get_task(name: str, db: Session = Depends(get_db)):
        return db.query(Tasks).filter(Tasks.project == name)

    #PUT /tasks (edit):
    @app.put("/tasks/{name}")
    def put_task(name: str, data: Tasks, db: Session = Depends(get_db)):
        if db.query(Projects).filter(Projects.name == name).first() is None:
            return "Project does not exist"
        else:
            project = db.query(Tasks).filter(Tasks.project == name)
            if project.first() is None:
                db.add(data)
                db.commit()
                return "Task Created"
            else:
                for task in project:
                    db.delete(task)
                    db.add(data)
                db.commit()
                return "Task Updated"

    #DELETE /tasks (delete):
    @app.delete("/tasks/{name}/{id}")
    def delete_task(name: str, id: int, db: Session = Depends(get_db)):
        if db.query(Projects).filter(Projects.name == name).first() is None:
            return "Project does not exist"
        else:
            project = db.query(Tasks).filter(Tasks.project == name)
            for task in project:
                if task.id == id:
                    db.delete(task)
                    db.commit()
                    return "Task Deleted"
            return "Task does not exist"
