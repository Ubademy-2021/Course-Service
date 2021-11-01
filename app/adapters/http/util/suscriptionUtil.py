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

    def check_suscription_course(db: Session, suscriptionCourse: SuscriptionCourse):
        suscriptionCourseRepository = SuscriptionCourseRepository(db)
        db_suscription_course = suscriptionCourseRepository.get_suscription_course(
            suscriptionCourse.courseId, suscriptionCourse.suscriptionId
        )
        if db_suscription_course:
            logger.warn("Suscription already has course")
            raise HTTPException(status_code=400, detail="Suscription already has course")
        courseRepository = CourseRepository(db)
        db_course = courseRepository.get_course(suscriptionCourse.courseId)
        if not db_course:
            logger.warn("Course " + str(suscriptionCourse.courseId) + " does not exist")
            raise HTTPException(
                status_code=400,
                detail="Course " + str(suscriptionCourse.courseId) + " does not exist",
            )
        suscriptionRepository = SuscriptionRepository(db)
        db_suscription = suscriptionRepository.get_suscription(suscriptionCourse.suscriptionId)
        if not db_suscription:
            logger.warn("Suscription " + str(suscriptionCourse.suscriptionId) + " does not exist")
            raise HTTPException(
                status_code=400,
                detail="Suscription " + str(suscriptionCourse.suscriptionId) + " does not exist",
            )
