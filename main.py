from unittest.mock import Base

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hey hey"}

@app.get("/home")
def read_home():
    return {"message": "Welcome to the home page"}

@app.get("/home/{name}")
def read_home_name(name: str):
    return {"message": f"Welcome to the home page, {name}"}


class Student(BaseModel):
    name: str
    age: int
    roll: int

@app.post("/create_student")
def create_student(student: Student):
    return {
        "name": student.name,
        "age": student.age,
        "roll": student.roll
    }