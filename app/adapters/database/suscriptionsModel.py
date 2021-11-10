from app.adapters.database.database import Base
from app.domain.suscriptions.suscription import SuscriptionCreate
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship


class SuscriptionDTO(Base):
    __tablename__ = "suscription"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, unique=True)
    price = Column(Float)

    courses = relationship("SuscriptionCourseDTO", back_populates="suscription")
    inscriptions = relationship("SuscriptionInscriptionDTO", back_populates="suscription")

    def initWithSuscriptionCreate(self, suscription: SuscriptionCreate):

        self.description = suscription.description
        self.price = suscription.price
