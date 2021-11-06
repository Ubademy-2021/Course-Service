from typing import List

from sqlalchemy.orm.session import Session
from app.adapters.database.collaboratorsModel import CollaboratorDTO
from app.adapters.database.coursesModel import CourseDTO
from app.domain.collaborators.collaborator import CollaboratorCreate
from app.domain.collaborators.collaboratorRepository import CollaboratorRepository
from app.adapters.http.util.userServiceUtil import UserServiceUtil
from app.core.logger import logger
from fastapi import HTTPException

from app.domain.courses.course import Course


class CollaboratorUtil:

    def check_collaborator(collaboratorRepository: CollaboratorRepository, collaborator: CollaboratorCreate):

        logger.info("Checking if user exists in user service")
        if not UserServiceUtil.checkUserExists(collaborator.userId):
            logger.error("User can not be add as a colaborator because it does not exist")
            raise HTTPException(status_code=400, detail="User does not exist")

        db_collaborator = collaboratorRepository.get_collaborator(collaborator.courseId, collaborator.userId)
        if db_collaborator:
            logger.warn("Collaborator already exists")
            raise HTTPException(
                status_code=400, detail="Collaborator already exists"
            )

    def createOwner(db: Session, course: CourseDTO, ownerId: int):

        logger.info("Checking if owner exists in user service")
        if not UserServiceUtil.checkUserExists(ownerId):
            logger.error("User can not be add as owner because it does not exist")
            raise HTTPException(status_code=400, detail="User does not exist")

        collaborator = CollaboratorDTO()
        collaborator.courseId = course.id
        collaborator.userId = ownerId
        collaborator.isOwner = True
        repo = CollaboratorRepository(db)
        return repo.add_collaborator(collaborator)
