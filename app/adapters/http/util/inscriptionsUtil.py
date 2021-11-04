from typing import List

from sqlalchemy.orm.session import Session
from app.adapters.database.courseInscriptionsModel import CourseInscriptionDTO
from app.adapters.database.coursesModel import CourseDTO
from app.domain.courseInscriptions.courseInscription import CourseInscriptionCreate
from app.domain.courseInscriptions.courseInscriptionRepository import CourseInscriptionRepository
from app.core.logger import logger
from fastapi import HTTPException


class CourseInscriptionUtil:

    def check_courseInscription(courseInscriptionRepository: CourseInscriptionRepository, courseInscription: CourseInscriptionCreate):
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
