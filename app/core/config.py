import os

POSTGRES_USER = "ocgerntcffbank"
POSTGRES_PASSWORD = "80d6b711e44a83cf460fe26f0fbe883e3f37571e2220f216811a30f40e95bfe9"
POSTGRES_SERVER = "ec2-35-169-204-98.compute-1.amazonaws.com"
POSTGRES_PORT = "5432"
POSTGRES_DB = "dfl4kcs7cejp7b"

DATABASE_URL = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

HEROKU_USER_SERVICE_BASE_URL = os.environ.get('HEROKU_USER_SERVICE_BASE_URL', "https://ubademy-user-service.herokuapp.com")

HEROKU_PAYMENTS_SERVICE_BASE_URL = os.environ.get('HEROKU_PAYMENTS_SERVICE_BASE_URL', "https://ubademy-payments-service.herokuapp.com")

SCORE_SAME_CATEGORY = 3
SCORE_SAME_COUNTRY = SCORE_SAME_CATEGORY * 3
