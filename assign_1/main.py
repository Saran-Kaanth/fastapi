from fastapi import FastAPI,Response,status,APIRouter
from fastapi.responses import JSONResponse
# from . import crud,schemas,database
import crud,schemas,database

router=APIRouter(prefix="/student",tags=["students"])
app=FastAPI()
app.include_router(router=APIRouter(prefix="/student",tags=["students"]))

@app.post("/create")
async def create_student_api(student_data:schemas.Student):
    student=crud.create_student(student_data)
    if student:
        return {"message":"Student added successfully"}
    return JSONResponse(content={"message":"student is already existed"},status_code=status.HTTP_400_BAD_REQUEST)

@app.get("/get_student/{student_id}")
async def get_student_by_id_api(student_id:int):
    student=crud.get_student_by_id(student_id)
    if student:
        return {"name":student["name"],
                "maths":student["maths"],
                "phy":student['phy'],
                "chem":student["chem"],
                "english":student["english"],
                "sanskrit":student["sanskrit"]}

    return JSONResponse(content="Student not found",status_code=status.HTTP_404_NOT_FOUND)

@app.get("/all_students",response_model=list[schemas.StudentOut])
def get_all_student_api():
    students=crud.get_all_students()
    if students:
        return crud.get_all_students()
    return JSONResponse(content="No Student Data",status_code=status.HTTP_404_NOT_FOUND)

@app.put("/update",response_model=schemas.StudentOut)
async def update_student_by_id_api(student_id:int,student_data:schemas.Student):
    update_student=crud.update_student_by_id(student_id,student_data)
    if update_student:
        return update_student
    return JSONResponse(content="Student not fount",status_code=status.HTTP_404_NOT_FOUND)

@app.delete("/delete/{student_id}")
async def delete_student_by_id(student_id:int):
    state=crud.delete_student_by_id(student_id)
    if state:
        return {"Student Deleted"}
    return JSONResponse(content="Student not found",status_code=status.HTTP_404_NOT_FOUND)