from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.adapters.database.database import Base
from app.domain.suscriptions.suscription import SuscriptionCreate

# catedra hacen Base=declarative_base()


class SuscriptionDTO(Base):
    __tablename__ = "suscription"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, unique=True)
    price = Column(Float)

    courses = relationship("SuscriptionCourseDTO", back_populates="suscription")

    def initWithSuscriptionCreate(self, suscription: SuscriptionCreate):

        self.description = suscription.description
        self.price = suscription.price
