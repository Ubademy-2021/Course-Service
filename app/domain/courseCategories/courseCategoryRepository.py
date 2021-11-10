from app.adapters.database.courseCategoriesModel import CourseCategoryDTO
from app.domain.courseCategories.courseCategory import CourseCategoryCreate
from sqlalchemy.orm import Session


class CourseCategoryRepository:
    def __init__(self, session: Session):
        self.session: Session = session

    def get_courseCategory(self, course_id: int, category_id: int):
        return self.session.query(CourseCategoryDTO).filter(CourseCategoryDTO.courseId == course_id).filter(CourseCategoryDTO.categoryId == category_id).first()

    def get_courses_by_category(self, category_id: int, skip: int = 0, limit: int = 100):
        return self.session.query(CourseCategoryDTO).filter(CourseCategoryDTO.categoryId == category_id).offset(skip).limit(limit).all()

    def get_categories_by_course(self, course_id: int, skip: int = 0, limit: int = 100):
        return self.session.query(CourseCategoryDTO).filter(CourseCategoryDTO.courseId == course_id).offset(skip).limit(limit).all()

    def get_courseCategories(self, skip: int = 0, limit: int = 100):
        return self.session.query(CourseCategoryDTO).offset(skip).limit(limit).all()

    def create_courseCategory(self, courseCategory: CourseCategoryCreate):
        session_courseCategory = CourseCategoryDTO()
        session_courseCategory.initWithCourseCategoryCreate(courseCategory)
        self.session.add(session_courseCategory)
        self.session.commit()
        self.session.refresh(session_courseCategory)
        return session_courseCategory
