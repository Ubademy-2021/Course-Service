from typing import List
from pydantic import BaseModel


class CourseCategoryBase(BaseModel):
    courseId: int
    categoryId: int


class CourseCategoryCreate(CourseCategoryBase):

    def isComplete(self):
        isNotComplete = (
            not self.courseId
            or not self.categoryId
        )
        return not isNotComplete


class CourseCategory(CourseCategoryBase):

    class Config:
        orm_mode = True
