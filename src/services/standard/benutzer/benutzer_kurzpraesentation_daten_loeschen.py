from src.constants import BENUTZER_KURZPRAESENTATION
from src.data.storage import get_benutzer_kurzpraesentation_folie, loeschen


def benutzer_kurzpraesentation_daten_loeschen(benutzer_id):
    benutzer_folie = get_benutzer_kurzpraesentation_folie(benutzer_id)
    print(benutzer_folie)
    if benutzer_folie and benutzer_folie != {}:
        loeschen(model=BENUTZER_KURZPRAESENTATION, user_id=benutzer_id)

