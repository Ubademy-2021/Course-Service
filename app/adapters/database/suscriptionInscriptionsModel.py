from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from app.adapters.database.database import Base
from app.domain.suscriptionInscriptions.suscriptionInscription import SuscriptionInscriptionCreate


class SuscriptionInscriptionDTO(Base):
    __tablename__ = "suscriptionInscription"

    suscriptionId = Column(Integer, ForeignKey("suscription.id"), index=True)
    userId = Column(Integer, primary_key=True, index=True)

    suscription = relationship("SuscriptionDTO", back_populates="inscriptions")

    def initWithSuscriptionInscriptionCreate(self, suscriptionInscription: SuscriptionInscriptionCreate):

        self.suscriptionId = suscriptionInscription.suscriptionId
        self.userId = suscriptionInscription.userId
        self.status = 'Active'
