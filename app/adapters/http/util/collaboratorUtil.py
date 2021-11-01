from typing import List

from sqlalchemy.orm.session import Session
from app.adapters.database.collaboratorsModel import CollaboratorDTO
from app.adapters.database.coursesModel import CourseDTO
from app.domain.collaborators.collaborator import CollaboratorCreate
from app.domain.collaborators.collaboratorRepository import CollaboratorRepository
from app.core.logger import logger
from fastapi import HTTPException

from app.domain.courses.course import Course


class CollaboratorUtil:

    def check_collaborator(collaboratorRepository: CollaboratorRepository, collaborator: CollaboratorCreate):
        db_collaborator = collaboratorRepository.get_collaborator(collaborator.courseId, collaborator.userId)
        if db_collaborator:
            logger.warn("Collaborator already exists")
            raise HTTPException(
                status_code=400, detail="Collaborator already exists"
            )

    def createOwner(db: Session, course: CourseDTO, ownerId: int):
        collaborator = CollaboratorDTO()
        collaborator.courseId = course.id
        collaborator.userId = ownerId
        collaborator.isOwner = True
        repo = CollaboratorRepository(db)
        return repo.add_collaborator(collaborator)
