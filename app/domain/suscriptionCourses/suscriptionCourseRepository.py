from sqlalchemy.orm import Session

from app.adapters.database.suscriptionCoursesModel import SuscriptionCourseDTO
from app.domain.suscriptionCourses.suscriptionCourse import SuscriptionCourse


class SuscriptionCourseRepository:
    def __init__(self, session: Session):
        self.session: Session = session

    def get_suscription_course(self, courseId, suscriptionId):
        return (
            self.session.query(SuscriptionCourseDTO)
            .filter(SuscriptionCourseDTO.courseId == courseId)
            .filter(SuscriptionCourseDTO.suscriptionId == suscriptionId)
            .first()
        )

    def get_courses_by_suscription(self, suscrptionId, skip: int = 0, limit: int = 100):
        return (
            self.session.query(SuscriptionCourseDTO)
            .filter(SuscriptionCourseDTO.suscriptionId == suscrptionId)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_suscriptions_by_course(self, courseId, skip: int = 0, limit: int = 100):
        return (
            self.session.query(SuscriptionCourseDTO)
            .filter(SuscriptionCourseDTO.courseId == courseId)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_suscription_course(self, suscriptionCourse: SuscriptionCourse):
        session_suscriptionCourse = SuscriptionCourseDTO()
        session_suscriptionCourse.initWithSuscriptionCourse(suscriptionCourse)
        self.session.add(session_suscriptionCourse)
        self.session.commit()
        self.session.refresh(session_suscriptionCourse)
        return session_suscriptionCourse
