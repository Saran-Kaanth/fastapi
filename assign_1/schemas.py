from pydantic import BaseModel


class Student(BaseModel):
    name:str
    maths:int|None=None
    phy:int|None=None
    chem:int|None=None
    english:int|None=None
    sanskrit:int|None=None

class StudentIn(Student):
    student_id:int

class StudentOut(Student):
    pass