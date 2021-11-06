from logging import log

from fastapi.exceptions import HTTPException
from app.core.config import HEROKU_USER_SERVICE_BASE_URL
import requests
from app.core.logger import logger


class UserServiceUtil:
    def makeUserRequest(userId):
        logger.info("Checking if user with id: " + str(userId) + " exists")

        url = HEROKU_USER_SERVICE_BASE_URL + "/api/users?user_id=" + str(userId)
        r = requests.get(url=url)

        if r.status_code != 200:
            logger.info("User not found")
            return False

        return True

    def check_user_exists(id):
        logger.info("Checking if user exists in user service")
        if not UserServiceUtil.makeUserRequest(id):
            logger.error("User does not exist")
            raise HTTPException(status_code=400, detail="User does not exist")
