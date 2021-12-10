import requests
from app.core.config import HEROKU_PAYMENTS_SERVICE_BASE_URL
from app.core.logger import logger
from fastapi.exceptions import HTTPException


class PaymentsServiceUtil:

    def changeSuscriptionPayment(userId: int, suscriptionId: int):

        logger.info("Changing payment in payments service")

        url = HEROKU_PAYMENTS_SERVICE_BASE_URL + "/deposit"
        data = {'senderId': userId, 'suscriptionId': suscriptionId}
        r = requests.post(url=url, json=data)

        logger.info(str(r.status_code) + ": " + r.text)

        if r.status_code != 201:
            logger.warning("Suscription could not be changed in payments service")
            raise HTTPException(status_code=400, detail="Suscription could not be changed")
