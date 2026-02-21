from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI() # Instance of FastAPI class

# 1st We have to create our Routing

@app.get("/") # We have created our home endpoint. / means Home endpoint. and @app.get is a decorator.
def home():
    return {"Message" : "Hello World"}

@app.get("/greet")
def greet():
    return {"Message" : "Hello Gireesh"}

# Path Parameters
@app.get("/greet/{name}")
def greet(name:str, age: Optional[int] = None): # name is a path parameter and we need to menctio it in the function
    return {"Message" : f"Hello {name} and Your age is {age}"}

# Query Parameters
@app.get("/greet1")
def greet(name:str, age:Optional[int] = None):
    return {"Message" : f"Hello {name} and Your age is {age}"}

# Request Body
class Student(BaseModel):
    name: str
    age: int
    roll: int
    course: str

@app.post("/create_student")
def create_student(student: Student):
    return{
        "name" : student.name,
        "age" : student.age,
        "roll" : student.roll,
        "course" : student.course
    }