from app.adapters.database.collaboratorsModel import CollaboratorDTO
from app.adapters.database.coursesModel import CourseDTO
from app.adapters.http.util.courseUtil import CourseUtil
from app.adapters.http.util.userServiceUtil import UserServiceUtil
from app.core.logger import logger
from app.domain.collaborators.collaborator import CollaboratorCreate
from app.domain.collaborators.collaboratorRepository import \
    CollaboratorRepository
from fastapi import HTTPException
from sqlalchemy.orm.session import Session


class CollaboratorUtil:

    def check_collaborator(session: Session, collaborator: CollaboratorCreate):

        UserServiceUtil.check_user_exists(collaborator.userId)

        CourseUtil.check_course_exists(session, collaborator.courseId)

        collaboratorRepository = CollaboratorRepository(session)
        db_collaborator = collaboratorRepository.get_collaborator(collaborator.courseId, collaborator.userId)
        if db_collaborator:
            logger.warning("Collaborator already exists")
            raise HTTPException(
                status_code=400, detail="Collaborator already exists"
            )

    def createOwner(session: Session, course: CourseDTO, ownerId: int):

        UserServiceUtil.check_user_exists(ownerId)

        collaborator = CollaboratorDTO()
        collaborator.courseId = course.id
        collaborator.userId = ownerId
        collaborator.isOwner = True
        repo = CollaboratorRepository(session)
        return repo.add_collaborator(collaborator)
