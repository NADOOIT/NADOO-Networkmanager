import os

from src.data.storage import get_benutzer_kurzpraesentation_folie


def kurzpraesentation_datei_loeschen(user_id):
    benutzer_folie = get_benutzer_kurzpraesentation_folie(user_id=user_id)
    if benutzer_folie:
        folien_path = benutzer_folie['folien_path']
        if os.path.exists(folien_path):
            os.remove(folien_path)
            print(f"Folie {folien_path} gelöscht.")
