from operator import lt
from pydantic import BaseModel, Field


class Student(BaseModel):
    name:str
    maths:int|None=Field(None,gt=0,le=100)
    phy:int|None=Field(None,gt=0,le=100)
    chem:int|None=Field(None,gt=0,le=100)
    english:int|None=Field(None,gt=0,le=100)
    sanskrit:int|None=Field(None,gt=0,le=100)

class StudentIn(Student):
    student_id:int|None=Field(ge=0)

class StudentOut(Student):
    pass