from typing import List
from app.adapters.database.suscriptionInscriptionsModel import SuscriptionInscriptionDTO
from app.adapters.http.util.courseUtil import CourseUtil
from app.adapters.http.util.suscriptionUtil import SuscriptionUtil

from app.domain.courseInscriptions.courseInscription import CourseInscriptionCreate
from app.domain.courseInscriptions.courseInscriptionRepository import CourseInscriptionRepository
from app.domain.suscriptions.suscriptionRepository import SuscriptionRepository
from app.core.logger import logger
from fastapi import HTTPException
from app.domain.courses.courseRepository import CourseRepository
from app.domain.suscriptionInscriptions.suscriptionInscription import SuscriptionInscription, SuscriptionInscriptionCreate
from app.domain.suscriptionInscriptions.suscriptionInscriptionRepository import SuscriptionInscriptionRepository
from app.adapters.http.util.userServiceUtil import UserServiceUtil


class CourseInscriptionUtil:

    def check_courseInscription(courseInscriptionRepository: CourseInscriptionRepository, courseInscription: CourseInscriptionCreate):

        UserServiceUtil.check_user_exists(courseInscription.userId)

        courseRepo = CourseRepository(courseInscriptionRepository.session)
        CourseUtil.check_course_exists(courseRepo, courseInscription.courseId)

        db_courseInscription = courseInscriptionRepository.get_courseInscription(courseInscription.courseId, courseInscription.userId)
        if db_courseInscription:
            logger.warn("Inscription already exists")
            raise HTTPException(
                status_code=400, detail="Inscription already exists"
            )

    def check_id_exists(courseInscriptionRepository: CourseInscriptionRepository, courseInscription: CourseInscriptionCreate):
        db_courseInscription = courseInscriptionRepository.get_courseInscription(courseInscription.courseId, courseInscription.userId)
        if not db_courseInscription:
            logger.warn("Inscription does not exist")
            raise HTTPException(
                status_code=400, detail="Inscription does not exist"
            )
        return db_courseInscription


class SuscriptionInscriptionUtil:

    def check_suscriptionInscription(suscriptionInscriptionRepository: SuscriptionInscriptionRepository, suscriptionInscription: SuscriptionInscriptionCreate):

        UserServiceUtil.check_user_exists(suscriptionInscription.userId)

        suscreptionRepo = SuscriptionRepository(suscriptionInscriptionRepository.session)
        SuscriptionUtil.check_suscription_exists(suscreptionRepo, suscriptionInscription.suscriptionId)

        db_suscriptionInscription = suscriptionInscriptionRepository.get_suscriptionInscription(suscriptionInscription.userId)
        if db_suscriptionInscription:
            logger.warn("Inscription already exists")
            raise HTTPException(
                status_code=400, detail="Inscription already exists"
            )

    def makeDefaultSuscription(userId: int):
        suscriptionInscription = SuscriptionInscriptionDTO()
        suscriptionInscription.suscriptionId = 0
        suscriptionInscription.userId = userId
        return suscriptionInscription
