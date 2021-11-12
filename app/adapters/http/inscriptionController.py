from app.adapters.database.courseInscriptionsModel import CourseInscriptionDTO
from app.adapters.database.database import SessionLocal
from app.adapters.http.util.inscriptionsUtil import (
    CourseInscriptionUtil, SuscriptionInscriptionUtil)
from app.adapters.http.util.userServiceUtil import UserServiceUtil
from app.core.logger import logger
from app.domain.courseInscriptions.courseInscription import (
    CourseInscription, CourseInscriptionCreate)
from app.domain.courseInscriptions.courseInscriptionRepository import \
    CourseInscriptionRepository
from app.domain.suscriptionInscriptions.suscriptionInscription import (
    SuscriptionInscription, SuscriptionInscriptionCreate)
from app.domain.suscriptionInscriptions.suscriptionInscriptionRepository import \
    SuscriptionInscriptionRepository
from app.domain.suscriptions.suscription import Suscription
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(tags=["inscriptions"])


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.critical("Internal Error: " + e.__str__())
    finally:
        db.close()


@router.post("/courses/inscription", response_model=CourseInscription)
def create_course_inscription(courseInscription: CourseInscriptionCreate, db: Session = Depends(get_db)):
    logger.info("Creating course inscription")
    if not courseInscription.isComplete():
        logger.warning("Required fields are not complete")
        raise HTTPException(status_code=400, detail="Required fields are not complete")
    repo = CourseInscriptionRepository(db)
    CourseInscriptionUtil.check_courseInscription(db, courseInscription)
    return repo.create_courseInscription(courseInscription=courseInscription)


@router.get("/courses/students/{course_id}")
def read_students(course_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info("Getting students list from course " + str(course_id))
    repo = CourseInscriptionRepository(db)
    courseInscriptions = repo.get_students_by_course(course_id, skip=skip, limit=limit)
    logger.debug("Getting " + str(len(courseInscriptions)) + " courseInscriptions")
    return UserServiceUtil.getUsersWithIds(list(map(CourseInscriptionDTO.getUserId, courseInscriptions)))


@router.put("/courses/inscription/cancel", response_model=CourseInscription)
def cancel_course_inscription(courseInscription: CourseInscriptionCreate, db: Session = Depends(get_db)):
    logger.info("Cancelling inscription")
    repo = CourseInscriptionRepository(db)
    db_inscription = CourseInscriptionUtil.check_id_exists(db, courseInscription)
    if (db_inscription.status == 'Cancelled'):
        logger.warning("Inscription already cancelled")
        raise HTTPException(
            status_code=400, detail=("Inscription already cancelled")
        )
    db_inscription.status = 'Cancelled'
    return repo.update_courseInscription_with_id(db_inscription)


@router.post("/suscriptions/inscription", response_model=SuscriptionInscription)
def create_suscription_inscription(suscriptionInscription: SuscriptionInscriptionCreate, db: Session = Depends(get_db)):
    logger.info("Creating suscription inscription")
    if not suscriptionInscription.isComplete():
        logger.warning("Required fields are not complete")
        raise HTTPException(status_code=400, detail="Required fields are not complete")
    repo = SuscriptionInscriptionRepository(db)
    SuscriptionInscriptionUtil.check_suscriptionInscription(db, suscriptionInscription)
    return repo.create_suscriptionInscription(suscriptionInscription)


@router.get("/suscriptions/inscription/{user_id}", response_model=Suscription)
def read_user_suscription(user_id: int, db: Session = Depends(get_db)):
    logger.info("Getting suscription from user " + str(user_id))
    repo = SuscriptionInscriptionRepository(db)

    UserServiceUtil.check_user_exists(user_id)

    suscriptionInscription = repo.get_suscriptionInscription(user_id)
    if not suscriptionInscription:
        suscriptionInscription = SuscriptionInscriptionUtil.makeDefaultSuscription(user_id)
    return suscriptionInscription.suscription
