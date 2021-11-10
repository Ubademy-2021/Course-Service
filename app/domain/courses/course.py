import datetime

from pydantic import BaseModel


class CourseBase(BaseModel):
    courseName: str
    duration: datetime.time
    inscriptionPrice: float


class CourseCreate(CourseBase):
    ownerId: int

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
