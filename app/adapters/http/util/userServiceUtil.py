from typing import List

import requests
from app.core.config import HEROKU_USER_SERVICE_BASE_URL
from app.core.logger import logger
from fastapi.exceptions import HTTPException


class UserServiceUtil:

    def getUserCategories(userId):
        logger.info("Getting categories for user with id: " + str(userId))

        url = HEROKU_USER_SERVICE_BASE_URL + "/api/categories/" + str(userId)
        r = requests.get(url=url)

        if r.status_code != 200:
            logger.warning("Error while getting categories")
            raise HTTPException(status_code=400, detail="Error while getting categories")

        response = r.json()

        categories_id = []
        for item in response:
            categories_id.append(item['id'])

        # Return user
        return categories_id

    def check_user_exists(id):
        logger.info("Checking if user with id: " + str(id) + " exists")

        url = HEROKU_USER_SERVICE_BASE_URL + "/api/users?user_id=" + str(id)
        r = requests.get(url=url)

        if r.status_code != 200:
            logger.warning("User not found")
            raise HTTPException(status_code=400, detail="User does not exist")

        # Return user
        return r.json()[0]

    def getActiveUsers():
        logger.info("Getting all active users")

        url = HEROKU_USER_SERVICE_BASE_URL + "/api/users/active"
        r = requests.get(url=url)

        if r.status_code != 200:
            logger.warning("Request error")
            raise HTTPException(status_code=400, detail="Request error")

        # Return users
        return r.json()

    def getUserFromUsers(users: List, userId):
        for user in users:
            if user["id"] == userId:
                print(user)
                return user

    def getUsersWithIds(ids: List):
        users = UserServiceUtil.getActiveUsers()
        returnUsers = []
        for id in ids:
            for user in users:
                if user["id"] == id:
                    returnUsers.append(user)
        return returnUsers
