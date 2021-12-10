import datetime
from typing import List

from pydantic import BaseModel


class CourseBase(BaseModel):
    courseName: str
    duration: datetime.time
    inscriptionPrice: float
    description: str


class CourseCreate(CourseBase):
    ownerId: int
    suscriptionId: int
    categoryIds: List[int]

    def isComplete(self):
        isNotComplete = (
            not self.courseName
            or not self.duration
            or not self.inscriptionPrice
        )
        return not isNotComplete


class Course(CourseBase):
    id: int
    createdDate: datetime.datetime
    status: str

    class Config:
        orm_mode = True
