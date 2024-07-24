import os
from dotenv import load_dotenv

load_dotenv()

BENUTZER_DATEN_FILE = os.getenv('BENUTZER_DATEN_FILE', 'data/db/benutzer_data.json')
FOLIEN_DATEN_FILE = os.getenv('FOLIEN_DATEN_FILE', 'data/db/folienvorlagen_data.json')
KURZPRAESENTATION_FOLIEN_DATEN_FILE = os.getenv('KURZPRAESENTATION_FOLIEN_DATEN_FILE',
                                                'data/db/benutzer_kurzpraesentation_data.json')
