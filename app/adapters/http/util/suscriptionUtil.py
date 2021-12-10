from app.adapters.database.suscriptionCoursesModel import SuscriptionCourseDTO
from app.adapters.http.util.courseUtil import CourseUtil
from app.core.logger import logger
from app.domain.suscriptionCourses.suscriptionCourse import SuscriptionCourse
from app.domain.suscriptionCourses.suscriptionCourseRepository import \
    SuscriptionCourseRepository
from app.domain.suscriptions.suscriptionRepository import SuscriptionRepository
from fastapi import HTTPException
from sqlalchemy.orm import Session


class SuscriptionUtil:

    def check_description(session: Session, description):
        suscriptionRepository = SuscriptionRepository(session)
        db_suscription = suscriptionRepository.get_suscription_by_description(description)
        if db_suscription:
            logger.warning("Description " + description + " already in use")
            raise HTTPException(
                status_code=400, detail="Description " + description + " already in use"
            )

    def check_id_exists(session: Session, suscription_id):
        suscriptionRepository = SuscriptionRepository(session)
        db_suscription = suscriptionRepository.get_suscription(suscription_id=suscription_id)
        if db_suscription is None:
            logger.warning("Suscription with id = " + str(suscription_id) + " not found")
            raise HTTPException(status_code=400, detail="Suscription not found")
        return db_suscription

    def check_suscription_exists(session: Session, id):
        repo = SuscriptionRepository(session)
        suscription = repo.get_suscription(id)
        if not suscription:
            logger.warning("Suscription does not exist")
            raise HTTPException(status_code=400, detail="Suscription does not exist")

    def check_suscription_course(session: Session, suscriptionCourse: SuscriptionCourse):

        CourseUtil.check_course_exists(session, suscriptionCourse.courseId)

        SuscriptionUtil.check_suscription_exists(session, suscriptionCourse.suscriptionId)

    def make_course_suscription(session: Session, courseId, suscriptionId):

        repo = SuscriptionCourseRepository(session)

        suscriptionCourse = SuscriptionCourse(
            suscriptionId=suscriptionId,
            courseId=courseId
        )
        repo.create_suscription_course(suscriptionCourse)
