from pydantic import BaseModel


class CourseInscriptionBase(BaseModel):
    courseId: int
    userId: int


class CourseInscriptionCreate(CourseInscriptionBase):

    def isComplete(self):
        isNotComplete = (
            not self.courseId
            or not self.userId
        )
        return not isNotComplete


class CourseInscription(CourseInscriptionBase):
    status: str

    class Config:
        orm_mode = True
