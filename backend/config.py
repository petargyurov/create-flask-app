import os

from dotenv import load_dotenv


class Config(object):
	load_dotenv()

	SUPPORT_CREDENTIALS = os.getenv('SUPPORT_CREDENTIALS')
	ORIGIN = os.getenv('ORIGIN')
	SECRET_KEY = os.getenv('SECRET_KEY')
