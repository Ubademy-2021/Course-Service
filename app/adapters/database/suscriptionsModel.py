from sqlalchemy import Column, Integer, String, Float
from app.adapters.database.database import Base
from app.domain.suscriptions.suscription import SuscriptionCreate

# catedra hacen Base=declarative_base()


class SuscriptionDTO(Base):
    __tablename__ = "suscription"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, unique=True)
    price = Column(Float)

    def initWithSuscriptionCreate(self, suscription: SuscriptionCreate):

        self.description = suscription.description
        self.price = suscription.price
