from sqlalchemy.orm import Session
from app.domain.courseInscriptions.courseInscription import CourseInscriptionCreate, CourseInscription
from app.adapters.database.courseInscriptionsModel import CourseInscriptionDTO


class CourseInscriptionRepository:
    def __init__(self, session: Session):
        self.session: Session = session

    def get_courseInscription(self, course_id: int, user_id: int):
        return self.session.query(CourseInscriptionDTO).filter(CourseInscriptionDTO.courseId == course_id).filter(CourseInscriptionDTO.userId == user_id).first()

    def get_students_by_course(self, course_id: int, skip: int = 0, limit: int = 100):
        return self.session.query(CourseInscriptionDTO).filter(CourseInscriptionDTO.courseId == course_id).filter(CourseInscriptionDTO.status == 'Active').offset(skip).limit(limit).all()

    def get_courseInscriptions(self, skip: int = 0, limit: int = 100):
        return self.session.query(CourseInscriptionDTO).offset(skip).limit(limit).all()

    def create_courseInscription(self, courseInscription: CourseInscriptionCreate):
        session_courseInscription = CourseInscriptionDTO()
        session_courseInscription.initWithCourseInscriptionCreate(courseInscription)
        self.session.add(session_courseInscription)
        self.session.commit()
        self.session.refresh(session_courseInscription)
        return session_courseInscription

    def update_courseInscription_with_id(self, courseInscription_updated: CourseInscriptionDTO):
        # Only use with courseInscription gotten from database
        self.session.add(courseInscription_updated)
        self.session.commit()
        self.session.refresh(courseInscription_updated)
        return courseInscription_updated

    def add_courseInscription(self, courseInscription: CourseInscriptionDTO):
        self.session.add(courseInscription)
        self.session.commit()
        self.session.refresh(courseInscription)
        return courseInscription
