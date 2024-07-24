from src.constants import BENUTZER_KURZPRAESENTATION
from src.data.storage import speichern


def benutzer_kurzpraesentation_daten_speichern(benutzer_daten):
    speichern(model=BENUTZER_KURZPRAESENTATION, data=benutzer_daten)
