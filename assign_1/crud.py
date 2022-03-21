import schemas,database
from fastapi.encoders import jsonable_encoder


def create_student(student_data:schemas.StudentIn):
    for student in database.student_data:
        if student["student_id"]==student_data.student_id or student["name"]==student_data.name:
            return False
    database.student_data.append(dict(student_data))
    return student_data

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



    