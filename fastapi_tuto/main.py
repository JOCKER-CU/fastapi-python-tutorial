from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel
from typing import Optional


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


# @app.get('/items/{item_id}')
# async def read_item(item_id: str):
#     return {"item_id": item_id}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id not in [1, 2, 3]:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id}

class Item(BaseModel):
    name: str
    price: float

@app.post("/items/")  # Make sure @app.post() is used
async def create_item(item: Item):
    return {"name": item.name, "price": item.price}


@app.get('/users/')
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

students = {
    1: {"name": "John Doe", "grade": "A", "age": 15, "class": "JSS3"},
    2: {"name": "Jane Smith", "grade": "B", "age": 14, "class": "JSS2"},
    3: {"name": "Michael Johnson", "grade": "A", "age": 16, "class": "SS1"},
    4: {"name": "Sylvester Stallone", "grade": "C", "age": 17, "class": "SS2"},
    5: {"name": "Tom Cruise", "grade": "A", "age": 15, "class": "JSS1"},
    6: {"name": "Will Smith", "grade": "B", "age": 14, "class": "JSS3"},

}

@app.get("/get-students/{student_id}")
async def get_students(student_id: int = Path(..., description="The ID of the student you want to view", gt=0, lt=2 )):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return students[student_id]  # ✅ Only return if the student exists


@app.get("/get-by-name/{student_id}")
def get_student(*, student_id: int, name: Optional[str] = None, test: int = 0):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    raise HTTPException(status_code=404, detail="Student not found")


class Student(BaseModel):
    name: str
    grade: str
    age: int
    class_: str

@app.post("/create-student/")
async def create_student(student: Student):
    # Generate a new student ID
    student_id = len(students) + 1
    # Add the new student to the dictionary
    students[student_id] = student.dict()
    return {"student_id": student_id, **students[student_id]}

@app.put("/update-student/{student_id}")
async def update_student(student_id: int, student: Student):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")

    # ✅ Update only non-null fields
    if student.name is not None:
        students[student_id]["name"] = student.name
    if student.grade is not None:
        students[student_id]["grade"] = student.grade
    if student.age is not None:
        students[student_id]["age"] = student.age
    if student.class_ is not None:
        students[student_id]["class_"] = student.class_

    return {"student_id": student_id, **students[student_id]}

@app.delete("/delete-student/{student_id}")
async def delete_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    del students[student_id]
    return {"message": "Student deleted successfully"}

@app.get("/get-students/")
async def get_students():
    return students








