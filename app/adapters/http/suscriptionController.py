from app.adapters.database.database import SessionLocal
from app.adapters.database.suscriptionsModel import SuscriptionDTO
from app.adapters.http.util.suscriptionUtil import SuscriptionUtil
from app.domain.suscriptions.suscription import SuscriptionCreate, Suscription
from app.domain.suscriptions.suscriptionRepository import SuscriptionRepository
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.logger import logger

router = APIRouter(tags=["suscriptions"])


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.critical("Internal Error: " + e.__str__())
    finally:
        db.close()


@router.post("/suscriptions", response_model=Suscription)
def create_suscription(suscription: SuscriptionCreate, db: Session = Depends(get_db)):
    logger.info("Creating suscription " + suscription.description)
    if not suscription.isComplete():
        logger.warn("Required fields are not complete")
        raise HTTPException(status_code=400, detail="Required fields are not complete")
    crud = SuscriptionRepository(db)
    SuscriptionUtil.check_description(crud, suscription.description)
    return crud.create_suscription(suscription=suscription)


@router.get("/suscriptions", response_model=List[Suscription])
def read_suscriptions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info("Getting suscriptions list")
    crud = SuscriptionRepository(db)
    suscriptions = crud.get_suscriptions(skip=skip, limit=limit)
    logger.debug("Getting " + str(suscriptions.count(SuscriptionDTO)) + " suscriptions")
    return suscriptions


@router.get("/suscriptions/{suscription_id}", response_model=Suscription)
def read_suscription(suscription_id: int, db: Session = Depends(get_db)):
    logger.info("Getting suscription with id = " + str(suscription_id))
    crud = SuscriptionRepository(db)
    db_suscription = SuscriptionUtil.check_id_exists(crud, suscription_id)
    return db_suscription
