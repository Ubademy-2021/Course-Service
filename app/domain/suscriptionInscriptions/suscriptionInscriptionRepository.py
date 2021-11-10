from app.adapters.database.suscriptionInscriptionsModel import \
    SuscriptionInscriptionDTO
from app.domain.suscriptionInscriptions.suscriptionInscription import \
    SuscriptionInscriptionCreate
from sqlalchemy.orm import Session


class SuscriptionInscriptionRepository:
    def __init__(self, session: Session):
        self.session: Session = session

    def get_suscriptionInscription(self, user_id: int):
        return self.session.query(SuscriptionInscriptionDTO).filter(SuscriptionInscriptionDTO.userId == user_id).first()

    def get_suscriptionInscriptions(self, skip: int = 0, limit: int = 100):
        return self.session.query(SuscriptionInscriptionDTO).offset(skip).limit(limit).all()

    def create_suscriptionInscription(self, suscriptionInscription: SuscriptionInscriptionCreate):
        session_suscriptionInscription = SuscriptionInscriptionDTO()
        session_suscriptionInscription.initWithSuscriptionInscriptionCreate(suscriptionInscription)
        self.session.add(session_suscriptionInscription)
        self.session.commit()
        self.session.refresh(session_suscriptionInscription)
        return session_suscriptionInscription

    def update_suscriptionInscription_with_id(self, suscriptionInscription_updated: SuscriptionInscriptionDTO):
        # Only use with suscriptionInscription gotten from database
        self.session.add(suscriptionInscription_updated)
        self.session.commit()
        self.session.refresh(suscriptionInscription_updated)
        return suscriptionInscription_updated
