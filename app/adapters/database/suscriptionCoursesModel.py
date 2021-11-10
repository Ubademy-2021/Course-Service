from app.adapters.database.database import Base
from app.domain.suscriptionCourses.suscriptionCourse import SuscriptionCourse
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey


class SuscriptionCourseDTO(Base):
    __tablename__ = "suscriptionCourse"

    courseId = Column(Integer, ForeignKey("course.id"), primary_key=True, index=True)
    suscriptionId = Column(Integer, ForeignKey("suscription.id"), primary_key=True, index=True)

    course = relationship("CourseDTO", back_populates="suscriptions")
    suscription = relationship("SuscriptionDTO", back_populates="courses")

    def initWithSuscriptionCourse(self, suscriptionCourse: SuscriptionCourse):

        self.courseId = suscriptionCourse.courseId
        self.suscriptionId = suscriptionCourse.suscriptionId

    def getCourse(self):
        return self.course
