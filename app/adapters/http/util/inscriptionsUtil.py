from app.adapters.database.suscriptionInscriptionsModel import \
    SuscriptionInscriptionDTO
from app.adapters.database.suscriptionsModel import SuscriptionDTO
from app.adapters.http.util.courseUtil import CourseUtil
from app.adapters.http.util.suscriptionUtil import SuscriptionUtil
from app.adapters.http.util.userServiceUtil import UserServiceUtil
from app.core.logger import logger
from app.domain.courseInscriptions.courseInscription import \
    CourseInscriptionCreate
from app.domain.courseInscriptions.courseInscriptionRepository import \
    CourseInscriptionRepository
from app.domain.suscriptionCourses.suscriptionCourseRepository import \
    SuscriptionCourseRepository
from app.domain.suscriptionInscriptions.suscriptionInscription import \
    SuscriptionInscriptionCreate
from app.domain.suscriptionInscriptions.suscriptionInscriptionRepository import \
    SuscriptionInscriptionRepository
from app.domain.suscriptions.suscriptionRepository import SuscriptionRepository
from fastapi import HTTPException
from sqlalchemy.orm import Session


class CourseInscriptionUtil:

    def check_courseInscription(session: Session, courseInscription: CourseInscriptionCreate):

        UserServiceUtil.check_user_exists(courseInscription.userId)

        CourseUtil.check_course_exists(session, courseInscription.courseId)

        courseInscriptionRepository = CourseInscriptionRepository(session)
        db_courseInscription = courseInscriptionRepository.get_courseInscription(courseInscription.courseId, courseInscription.userId)
        if db_courseInscription and db_courseInscription.status == "Active":
            logger.warning("Inscription already exists")
            raise HTTPException(
                status_code=400, detail="Inscription already exists"
            )

        scRepo = SuscriptionCourseRepository(session)
        sc = scRepo.get_suscriptions_by_course(courseInscription.courseId)
        siRepo = SuscriptionInscriptionRepository(session)
        si = siRepo.get_suscriptionInscription(courseInscription.userId)

        userSuscriptionId = 1
        if si:
            userSuscriptionId = si.suscriptionId
        if sc:
            if sc.suscriptionId > userSuscriptionId:
                logger.warning("Inscription not allowed because of suscription level")
                raise HTTPException(
                    status_code=400, detail="Inscription not allowed because of suscription level"
                )

    def check_id_exists(session: Session, courseInscription: CourseInscriptionCreate):
        courseInscriptionRepository = CourseInscriptionRepository(session)
        db_courseInscription = courseInscriptionRepository.get_courseInscription(courseInscription.courseId, courseInscription.userId)
        if not db_courseInscription:
            logger.warning("Inscription does not exist")
            raise HTTPException(
                status_code=400, detail="Inscription does not exist"
            )
        return db_courseInscription


class SuscriptionInscriptionUtil:

    def check_suscriptionInscription(session: Session, suscriptionInscription: SuscriptionInscriptionCreate):

        UserServiceUtil.check_user_exists(suscriptionInscription.userId)

        SuscriptionUtil.check_suscription_exists(session, suscriptionInscription.suscriptionId)

    def makeDefaultSuscription(session: Session, userId: int):
        suscriptionInscription = SuscriptionInscriptionDTO()
        suscriptionInscription.suscriptionId = 1
        suscriptionInscription.userId = userId
        repo = SuscriptionRepository(session)
        suscriptionInscription.suscription = repo.get_suscription(1)
        return suscriptionInscription
