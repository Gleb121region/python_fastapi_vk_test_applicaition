import os

from dotenv import load_dotenv

load_dotenv()

AUTH_MICROSERVICE_URL = os.environ.get("AUTH_MICROSERVICE_URL")
NOTES_MICROSERVICE_URL = os.environ.get("NOTES_MICROSERVICE_URL")

CHAT_MICROSERVICE_URL_WS = os.environ.get("CHAT_MICROSERVICE_URL_WS")
