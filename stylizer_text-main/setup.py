from dotenv import load_dotenv
import os

LOCAL_VARIABLES_FILE = ".env"
env = load_dotenv(LOCAL_VARIABLES_FILE)

DATABASE_USER = os.environ["DATABASE_USER"]
DATABASE_PASSWORD = os.environ["DATABASE_PASSWORD"]
DATABASE_NAME = os.environ["DATABASE_NAME"]
DATABASE_URI = os.environ["DATABASE_URI"]
DATABASE_PORT = os.environ["DATABASE_PORT"]

# CELERY_URI = os.environ["CELERY_URI"]
# CELERY_PORT = os.environ["CELERY_PORT"]

TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]

AUTH_SECRET_KEY = os.environ["AUTH_SECRET_KEY"]
AUTH_ALGORITHM = os.environ["AUTH_ALGORITHM"]
AUTH_ACCESS_TOKEN_EXPIRE_MINUTES = os.environ["AUTH_ACCESS_TOKEN_EXPIRE_MINUTES"]

# LIMIT_CONTEXT_LENGTH = os.environ["LIMIT_CONTEXT_LENGTH"]
# LIMIT_PROMPT_LENGTH = os.environ["LIMIT_PROMPT_LENGTH"]


OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://%s:%s@%s:%s/%s" % (
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_URI,
    DATABASE_PORT,
    DATABASE_NAME,
)

# CELERY_URL = "redis://%s:%s" % (
#     CELERY_URI,
#     CELERY_PORT
# )

settings = {"db": {"uri": SQLALCHEMY_DATABASE_URL},
            # "task_queue" : { "uri": CELERY_URL },
            "auth": {"secret_key": AUTH_SECRET_KEY,
                     "algorithm": AUTH_ALGORITHM,
                     "access_token_expire_minutes": AUTH_ACCESS_TOKEN_EXPIRE_MINUTES},
            "openai": {"api_key": OPENAI_API_KEY},
            "telegram": {"api_key": TELEGRAM_API_KEY}}