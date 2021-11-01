from sqlalchemy.orm import Session
from app.domain.suscriptions.suscription import SuscriptionCreate, Suscription
from app.adapters.database.suscriptionsModel import SuscriptionDTO


class SuscriptionRepository:
    def __init__(self, session: Session):
        self.session: Session = session

    def get_suscription(self, suscription_id: int):
        return self.session.query(SuscriptionDTO).filter(SuscriptionDTO.id == suscription_id).first()

    def get_suscription_by_description(self, desription: str):
        return self.session.query(SuscriptionDTO).filter(SuscriptionDTO.description == desription).first()

    def get_suscriptions(self, skip: int = 0, limit: int = 100):
        return self.session.query(SuscriptionDTO).offset(skip).limit(limit).all()

    def create_suscription(self, suscription: SuscriptionCreate):
        session_suscription = SuscriptionDTO()
        session_suscription.initWithSuscriptionCreate(suscription)
        self.session.add(session_suscription)
        self.session.commit()
        self.session.refresh(session_suscription)
        return session_suscription

    def update_suscription_with_id(self, suscription_updated: Suscription):
        # Only use with suscription gotten from database
        self.session.add(suscription_updated)
        self.session.commit()
        self.session.refresh(suscription_updated)
        return suscription_updated
