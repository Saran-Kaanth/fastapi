import schemas,database
from fastapi.encoders import jsonable_encoder


def create_student(student_data:schemas.Student):
    student_ids=[]
    for student in database.student_data:
        student_ids.append(student["student_id"])
        if student["name"]==student_data.name:
            return False
    print(max(student_ids))
    new_id=max(student_ids)+1
    new_student=schemas.StudentIn(student_id=new_id,**student_data.dict())
    database.student_data.append(dict(new_student))
    return new_student

def get_student_by_id(student_id:int):
    for student in database.student_data:
        if student["student_id"]==student_id:
            return student
    return False

def get_all_students():
    return database.student_data

def update_student_by_id(student_id:int,student_data:schemas.Student):
    student_update_data=jsonable_encoder(student_data)
    for student in database.student_data:
        if student["student_id"]==student_id:
            student.update(student_update_data)
            return student
    return False

def delete_student_by_id(student_id:int):
    for student in database.student_data:
        if student["student_id"]==student_id:
            database.student_data.remove(student)
            return True
    return False



    