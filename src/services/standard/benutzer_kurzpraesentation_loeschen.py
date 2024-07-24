from src.data.storage import benutzer_speichern, get_benutzer_liste, get_benutzer_kurzpraesentation_folie, \
    loeschen_benutzer_kurzpraesentation_daten

from . import kurzpraesentation_folie_loeschen


def benutzer_kurzpraesentation_loeschen(benutzer_id):
    benutzer_folie = get_benutzer_kurzpraesentation_folie(benutzer_id)

    if benutzer_folie:
        kurzpraesentation_folie_loeschen(benutzer_folie)

    loeschen_benutzer_kurzpraesentation_daten(benutzer_id)
