from app.adapters.database.collaboratorsModel import CollaboratorDTO
from app.adapters.database.database import SessionLocal
from app.adapters.http.util.collaboratorUtil import CollaboratorUtil
from app.adapters.http.util.userServiceUtil import UserServiceUtil
from app.core.logger import logger
from app.domain.collaborators.collaborator import (Collaborator,
                                                   CollaboratorCreate)
from app.domain.collaborators.collaboratorRepository import \
    CollaboratorRepository
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(tags=["collaborators"])


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.critical("Internal Error: " + e.__str__())
    finally:
        db.close()


@router.get("/collaborators")
def read_all_collaborators(db: Session = Depends(get_db)):
    logger.info("Getting all collaborators")
    repo = CollaboratorRepository(db)
    collaborators = repo.get_all_collaborators()
    logger.debug("Getting " + str(len(collaborators)) + " collaborators")
    return UserServiceUtil.getUsersWithIds(list(set(map(CollaboratorDTO.getUserId, collaborators))))


@router.post("/collaborators", response_model=Collaborator)
def create_collaborator(collaborator: CollaboratorCreate, db: Session = Depends(get_db)):
    logger.info("Creating collaborator")

    if not collaborator.isComplete():
        logger.warning("Required fields are not complete")
        raise HTTPException(status_code=400, detail="Required fields are not complete")
    repo = CollaboratorRepository(db)
    CollaboratorUtil.check_collaborator(db, collaborator)

    return repo.create_collaborator(collaborator=collaborator)


@router.get("/collaborators/{course_id}")
def read_collaborators(course_id, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info("Getting collaborators list from course " + str(course_id))
    repo = CollaboratorRepository(db)
    collaborators = repo.get_collaborators_by_course(course_id, skip=skip, limit=limit)
    logger.debug("Getting " + str(len(collaborators)) + " collaborators")
    return UserServiceUtil.getUsersWithIds(list(map(CollaboratorDTO.getUserId, collaborators)))
