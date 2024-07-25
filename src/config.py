import os
from dotenv import load_dotenv

load_dotenv()

BENUTZER_DATEN_FILE = os.getenv('BENUTZER_DATEN_FILE', '')
FOLIEN_DATEN_FILE = os.getenv('FOLIEN_DATEN_FILE', '')
KURZPRAESENTATION_FOLIEN_DATEN_FILE = os.getenv('KURZPRAESENTATION_FOLIEN_DATEN_FILE', '')
