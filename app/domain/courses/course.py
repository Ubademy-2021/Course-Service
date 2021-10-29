from typing import List
from pydantic import BaseModel
import datetime


class CourseBase(BaseModel):
    courseName: str
    categoryId: int
    duration: datetime.time
    inscriptionPrice: float


class CourseCreate(CourseBase):
    def isComplete(self):
        isNotComplete = (
            not self.courseName
            or not self.categoryId
            or not self.duration
            or not self.inscriptionPrice
        )
        return not isNotComplete


class Course(CourseBase):
    id: int
    cratedDate: datetime.datetime
    status: str

    class Config:
        orm_mode = True
