# config.py
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv('API_URL')
TEST_CREDENTIALS = {
    "username": os.getenv('TEST_USERNAME'),
    "password": os.getenv('TEST_PASSWORD')
}