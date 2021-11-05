from typing import List
from pydantic import BaseModel


class SuscriptionInscriptionBase(BaseModel):
    suscriptionId: int
    userId: int


class SuscriptionInscriptionCreate(SuscriptionInscriptionBase):

    def isComplete(self):
        isNotComplete = (
            not self.suscriptionId
            or not self.userId
        )
        return not isNotComplete


class SuscriptionInscription(SuscriptionInscriptionBase):

    class Config:
        orm_mode = True
