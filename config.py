import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///site.db')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False