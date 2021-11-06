from app.adapters.http.util.courseUtil import CourseUtil
from app.domain.suscriptionCourses.suscriptionCourse import SuscriptionCourse
from app.domain.suscriptionCourses.suscriptionCourseRepository import SuscriptionCourseRepository
from app.domain.suscriptions.suscriptionRepository import SuscriptionRepository
from app.domain.courses.courseRepository import CourseRepository
from app.core.logger import logger
from fastapi import HTTPException
from sqlalchemy.orm import Session


class SuscriptionUtil:

    def check_description(suscriptionRepository: SuscriptionRepository, description):
        db_suscription = suscriptionRepository.get_suscription_by_description(description)
        if db_suscription:
            logger.warn("Description " + description + " already in use")
            raise HTTPException(
                status_code=400, detail="Description " + description + " already in use"
            )

    def check_id_exists(suscriptionRepository: SuscriptionRepository, suscription_id):
        db_suscription = suscriptionRepository.get_suscription(suscription_id=suscription_id)
        if db_suscription is None:
            logger.warning("Suscription with id = " + str(suscription_id) + " not found")
            raise HTTPException(status_code=404, detail="Suscription not found")
        return db_suscription

    def check_suscription_exists(repo: SuscriptionRepository, id):
        suscription = repo.get_suscription(id)
        if not suscription:
            logger.error("Suscription does not exist")
            raise HTTPException(status_code=400, detail="Suscription does not exist")

    def check_suscription_course(db: Session, suscriptionCourse: SuscriptionCourse):

        courseRepository = CourseRepository(db)
        CourseUtil.check_course_exists(courseRepository, suscriptionCourse.courseId)

        suscriptionRepository = SuscriptionRepository(db)
        SuscriptionUtil.check_suscription_exists(suscriptionRepository, suscriptionCourse.suscriptionId)

        suscriptionCourseRepository = SuscriptionCourseRepository(db)
        db_suscription_course = suscriptionCourseRepository.get_suscription_course(
            suscriptionCourse.courseId, suscriptionCourse.suscriptionId
        )
        if db_suscription_course:
            logger.warn("Suscription already has course")
            raise HTTPException(status_code=400, detail="Suscription already has course")
