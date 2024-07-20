import os
from dotenv import load_dotenv

load_dotenv()

DATA_FILE_PATH = os.getenv('DATA_FILE_PATH', 'data/db/data.json')
