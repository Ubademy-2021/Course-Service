from app.adapters.database.database import Base
from app.domain.collaborators.collaborator import CollaboratorCreate
from sqlalchemy import Boolean, Column, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey


class CollaboratorDTO(Base):
    __tablename__ = "collaborator"

    courseId = Column(Integer, ForeignKey("course.id"), primary_key=True, index=True)
    userId = Column(Integer, primary_key=True, index=True)
    isOwner = Column(Boolean)

    course = relationship("CourseDTO", back_populates="collaborators")

    def initWithCollaboratorCreate(self, collaborator: CollaboratorCreate):

        self.courseId = collaborator.courseId
        self.userId = collaborator.userId
        self.isOwner = False

    def getUserId(self):
        return self.userId

    def getCourse(self):
        return self.course
