from sqlalchemy import Column, Integer, String, DateTime, Time, Float
from sqlalchemy.orm import relationship
from app.adapters.database.database import Base
from app.domain.courses.course import CourseCreate
import datetime

# catedra hacen Base=declarative_base()


class CourseDTO(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True, index=True)
    courseName = Column(String, unique=True)
    createdDate = Column(DateTime)
    duration = Column(Time)
    inscriptionPrice = Column(Float)
    status = Column(String)

    suscriptions = relationship("SuscriptionCourseDTO", back_populates="course")

    def initWithCourseCreate(self, course: CourseCreate):

        self.courseName = course.courseName
        self.createdDate = datetime.datetime.now()
        self.duration = course.duration
        self.inscriptionPrice = course.inscriptionPrice
        self.status = "Active"
