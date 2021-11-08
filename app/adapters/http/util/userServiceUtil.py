from logging import log

from fastapi.exceptions import HTTPException
from app.core.config import HEROKU_USER_SERVICE_BASE_URL
import requests
from app.core.logger import logger


class UserServiceUtil:

    def getUserCategories(userId):
        logger.info("Getting categories for user with id: " + str(userId))

        url = HEROKU_USER_SERVICE_BASE_URL + "/api/categories/" + str(userId)
        r = requests.get(url=url)

        if r.status_code != 200:
            logger.warn("Error while getting categories")
            raise HTTPException(status_code=400, detail="Error while getting categories")

        response = r.json()

        categories_id = []
        for item in response:
            categories_id.append(item['categoryId'])

        # Return user
        return categories_id

    def check_user_exists(id):
        logger.info("Checking if user with id: " + str(id) + " exists")

        url = HEROKU_USER_SERVICE_BASE_URL + "/api/users?user_id=" + str(id)
        r = requests.get(url=url)

        if r.status_code != 200:
            logger.warn("User not found")
            raise HTTPException(status_code=400, detail="User does not exist")

        # Return user
        return r.json()[0]
