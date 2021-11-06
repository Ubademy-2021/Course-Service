from logging import log
from app.core.config import HEROKU_USER_SERVICE_BASE_URL
import requests
from app.core.logger import logger


class UserServiceUtil:
    def checkUserExists(userId):
        logger.info("Checking if user with id: " + str(userId) + " exists")

        url = HEROKU_USER_SERVICE_BASE_URL + "/api/users?user_id=" + str(userId)
        r = requests.get(url=url)

        if r.status_code != 200:
            logger.info("User not found")
            return False

        return True