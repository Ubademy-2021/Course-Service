"""
from databases import DatabaseURL
from starlette.config import Config
from starlette.datastructures import Secret


config = Config(".env")
PROJECT_NAME = "phresh"
VERSION = "1.0.0"
API_PREFIX = "/api"
SECRET_KEY = config("SECRET_KEY", cast=Secret, default="CHANGEME")
POSTGRES_USER = config("POSTGRES_USER", cast=str)
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=Secret)
POSTGRES_SERVER = config("POSTGRES_SERVER", cast=str, default="db")
POSTGRES_PORT = config("POSTGRES_PORT", cast=str, default="5432")
POSTGRES_DB = config("POSTGRES_DB", cast=str)
DATABASE_URL = config(
  "DATABASE_URL",
  cast=DatabaseURL,
  default=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
"""

POSTGRES_USER = "ocgerntcffbank"
POSTGRES_PASSWORD = "80d6b711e44a83cf460fe26f0fbe883e3f37571e2220f216811a30f40e95bfe9"
POSTGRES_SERVER = "ec2-35-169-204-98.compute-1.amazonaws.com"
POSTGRES_PORT = "5432"
POSTGRES_DB = "dfl4kcs7cejp7b"

# DATABASE_URL = "    postgres://ocgerntcffbank:80d6b711e44a83cf460fe26f0fbe883e3f37571e2220f216811a30f40e95bfe9@ec2-35-169-204-98.compute-1.amazonaws.com:5432/dfl4kcs7cejp7b"

DATABASE_URL = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
