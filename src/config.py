import os
from dotenv import load_dotenv

load_dotenv()

BENUTZER_DATEN = os.getenv('BENUTZER_DATEN', 'data/benutzer.json')
FOLIEN_DATEN = os.getenv('FOLIEN_DATEN', 'data/folienvorlagen.json')
KURZPRAESENTATION_FOLIEN_DATEN = os.getenv('KURZPRAESENTATION_FOLIEN_DATEN', 'data/Kurzpraesetation_folien.json')
