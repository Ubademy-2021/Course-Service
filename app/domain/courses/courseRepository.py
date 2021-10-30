from sqlalchemy.orm import Session
from app.domain.courses.course import CourseCreate, Course
from app.adapters.database.coursesModel import CourseDTO
from app.domain.exceptions import CourseNotFoundError


class CourseRepository:
    def __init__(self, session: Session):
        self.session: Session = session

    def get_course(self, course_id: int):
        return self.session.query(CourseDTO).filter(CourseDTO.id == course_id).first()

    def get_course_by_name(self, courseName: str):
        return self.session.query(CourseDTO).filter(CourseDTO.courseName == courseName).first()

    def get_courses(self, skip: int = 0, limit: int = 100):
        return self.session.query(CourseDTO).offset(skip).limit(limit).all()

    def create_course(self, course: CourseCreate):
        session_course = CourseDTO()
        session_course.initWithCourseCreate(course)
        self.session.add(session_course)
        self.session.commit()
        self.session.refresh(session_course)
        return session_course

    def update_course(self, db_course_id: int, course_updated: CourseCreate):
        # Get the existing data
        db_course = self.session.query(CourseDTO).filter(CourseDTO.id == db_course_id).one_or_none()

        if db_course is None:
            raise CourseNotFoundError()

        # Update model class variable from requested fields
        for var, value in vars(course_updated).items():
            setattr(db_course, var, value) if value or str(value) == 'False' else None

        self.session.add(db_course)
        self.session.commit()
        self.session.refresh(db_course)
        return db_course

    def update_course_with_id(self, course_updated: Course):
        # Only use with course gotten from database
        self.session.add(course_updated)
        self.session.commit()
        self.session.refresh(course_updated)
        return course_updated
