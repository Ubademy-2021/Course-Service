from typing import List
from pydantic import BaseModel


class CollaboratorBase(BaseModel):
    courseId: int
    userId: int


class CollaboratorCreate(CollaboratorBase):

    def isComplete(self):
        isNotComplete = (
            not self.courseId
            or not self.userId
        )
        return not isNotComplete


class Collaborator(CollaboratorBase):
    isOwner: bool

    class Config:
        orm_mode = True
