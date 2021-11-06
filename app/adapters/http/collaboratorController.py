from app.adapters.database.database import SessionLocal
from app.adapters.database.collaboratorsModel import CollaboratorDTO
from app.adapters.http.util.collaboratorUtil import CollaboratorUtil
from app.adapters.http.util.userServiceUtil import UserServiceUtil
from app.domain.collaborators.collaborator import CollaboratorCreate, Collaborator
from app.domain.collaborators.collaboratorRepository import CollaboratorRepository
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.logger import logger

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


@router.post("/collaborators", response_model=Collaborator)
def create_collaborator(collaborator: CollaboratorCreate, db: Session = Depends(get_db)):
    logger.info("Creating collaborator")

    if not collaborator.isComplete():
        logger.warn("Required fields are not complete")
        raise HTTPException(status_code=400, detail="Required fields are not complete")
    repo = CollaboratorRepository(db)
    CollaboratorUtil.check_collaborator(repo, collaborator)

    return repo.create_collaborator(collaborator=collaborator)


@router.get("/collaborators/{course_id}", response_model=List[Collaborator])
def read_collaborators(course_id, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info("Getting collaborators list from course " + str(course_id))
    repo = CollaboratorRepository(db)
    collaborators = repo.get_collaborators_by_course(course_id, skip=skip, limit=limit)
    logger.debug("Getting " + str(collaborators.count(CollaboratorDTO)) + " collaborators")
    return collaborators
