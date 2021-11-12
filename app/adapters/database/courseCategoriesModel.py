from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from app.adapters.database.database import Base
from app.domain.courseCategories.courseCategory import CourseCategoryCreate


class CourseCategoryDTO(Base):
    __tablename__ = "courseCategory"

    courseId = Column(Integer, ForeignKey("course.id"), primary_key=True, index=True)
    categoryId = Column(Integer, ForeignKey("category.id"), primary_key=True, index=True)

    course = relationship("CourseDTO", back_populates="categories")
    category = relationship("CategoryDTO", back_populates="courses")

    def initWithCourseCategoryCreate(self, courseCategory: CourseCategoryCreate):

        self.courseId = courseCategory.courseId
        self.categoryId = courseCategory.categoryId

    def getCourse(self):
        return self.course

    def getCategory(self):
        return self.category
