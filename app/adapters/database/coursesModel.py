import datetime

from app.adapters.database.database import Base
from app.domain.courses.course import CourseCreate
from sqlalchemy import Column, DateTime, Float, Integer, String, Time
from sqlalchemy.orm import relationship

# catedra hacen Base=declarative_base()


class CourseDTO(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True, index=True)
    courseName = Column(String, unique=True)
    description = Column(String)
    createdDate = Column(DateTime)
    duration = Column(Time)
    inscriptionPrice = Column(Float)
    status = Column(String)

    suscriptions = relationship("SuscriptionCourseDTO", back_populates="course")
    collaborators = relationship("CollaboratorDTO", back_populates="course")
    inscriptions = relationship("CourseInscriptionDTO", back_populates="course")
    categories = relationship("CourseCategoryDTO", back_populates="course")

    def initWithCourseCreate(self, course: CourseCreate):

        self.courseName = course.courseName
        self.description = course.description
        self.createdDate = datetime.datetime.now()
        self.duration = course.duration
        self.inscriptionPrice = course.inscriptionPrice
        self.status = "Active"
