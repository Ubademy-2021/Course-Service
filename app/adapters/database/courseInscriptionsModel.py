from app.adapters.database.database import Base
from app.domain.courseInscriptions.courseInscription import \
    CourseInscriptionCreate
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey


class CourseInscriptionDTO(Base):
    __tablename__ = "courseInscription"

    courseId = Column(Integer, ForeignKey("course.id"), primary_key=True, index=True)
    userId = Column(Integer, primary_key=True, index=True)
    status = Column(String)

    course = relationship("CourseDTO", back_populates="inscriptions")

    def initWithCourseInscriptionCreate(self, courseInscription: CourseInscriptionCreate):

        self.courseId = courseInscription.courseId
        self.userId = courseInscription.userId
        self.status = 'Active'

    def getUserId(self):
        return self.userId

    def getCourse(self):
        return self.course
