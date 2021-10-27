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
"""
POSTGRES_USER = "dnelosexrgszoz"
POSTGRES_PASSWORD = "d0bcea04baf4cb598c261aea150aed55871cc7e65778b78c29b6201f98ddc98a"
POSTGRES_SERVER = "ec2-34-194-123-31.compute-1.amazonaws.com"
POSTGRES_PORT = "5432"
POSTGRES_DB = "dcmlmhd3ipa6a5"

# DATABASE_URL = "postgres://dnelosexrgszoz:d0bcea04baf4cb598c261aea150aed55871cc7e65778b78c29b6201f98ddc98a@ec2-34-194-123-31.compute-1.amazonaws.com:5432/dcmlmhd3ipa6a5"

DATABASE_URL = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
"""
