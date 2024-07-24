import os
from dotenv import load_dotenv

load_dotenv()

BENUTZER_DATEN = os.getenv('BENUTZER_DATEN', 'data/db/benutzer.json')
FOLIEN_DATEN = os.getenv('FOLIEN_DATEN', 'data/db/folienvorlagen.json')
KURZPRAESENTATION_FOLIEN_DATEN = os.getenv('KURZPRAESENTATION_FOLIEN_DATEN', 'data/db/Kurzpraesetation_folien.json')
