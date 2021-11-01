from typing import List
from pydantic import BaseModel


class SuscriptionBase(BaseModel):
    description: str
    price: float


class SuscriptionCreate(SuscriptionBase):
    def isComplete(self):
        isNotComplete = (
            not self.description
            or not self.price
        )
        return not isNotComplete


class Suscription(SuscriptionBase):
    id: int

    class Config:
        orm_mode = True
