import datetime
from typing import List, Optional

from pydantic import BaseModel


class CourseBase(BaseModel):
    courseName: str
    duration: datetime.time
    description: str
    videos: Optional[str]


class CourseCreate(CourseBase):
    ownerId: int
    suscriptionId: int
    categoryIds: List[int]

    def isComplete(self):
        isNotComplete = (
            not self.courseName
            or not self.duration
        )
        return not isNotComplete


class CourseUpdate(CourseBase):
    suscriptionId: int


class Course(CourseBase):
    id: int
    createdDate: datetime.datetime
    status: str

    class Config:
        orm_mode = True
