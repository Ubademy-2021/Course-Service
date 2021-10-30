from sqlalchemy.orm import Session
from app.domain.courses.course import CourseCreate, Course
from app.adapters.database.coursesModel import CourseDTO


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

    def update_course_with_id(self, course_updated: Course):
        # Only use with course gotten from database
        self.session.add(course_updated)
        self.session.commit()
        self.session.refresh(course_updated)
        return course_updated
