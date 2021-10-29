from sqlalchemy import Column, Integer, String, DateTime, Time, Float
from app.adapters.database.database import Base
from app.domain.courses.course import CourseCreate
import datetime

# catedra hacen Base=declarative_base()


class CourseDTO(Base):
    __tablename__ = "Course"

    id = Column(Integer, primary_key=True, index=True)
    courseName = Column(String, unique=True)
    categoryId = Column(Integer)
    createdDate = Column(DateTime)
    duration = Column(Time)
    inscriptionPrice = Column(Float)
    status = Column(String)

    def initWithCourseCreate(self, course: CourseCreate):

        self.courseName = course.courseName
        self.categoryId = course.categoryId
        self.createdDate = datetime.datetime.now()
        self.duration = course.duration
        self.inscriptionPrice = course.inscriptionPrice
        self.status = "Active"
