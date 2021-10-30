from app.domain.suscriptions.suscriptionRepository import SuscriptionRepository
from app.core.logger import logger
from fastapi import HTTPException


class SuscriptionUtil:

    def check_description(suscriptionRepository: SuscriptionRepository, description):
        db_suscription = suscriptionRepository.get_suscription_by_description(description)
        if db_suscription:
            logger.warn("Description " + description + " already in use")
            raise HTTPException(
                status_code=400, detail="Description " + description + " already in use"
            )

    def check_id_exists(suscriptionRepository: SuscriptionRepository, suscription_id):
        db_suscription = suscriptionRepository.get_suscription(suscription_id=suscription_id)
        if db_suscription is None:
            logger.warning("Suscription with id = " + str(suscription_id) + " not found")
            raise HTTPException(status_code=404, detail="Suscription not found")
        return db_suscription
