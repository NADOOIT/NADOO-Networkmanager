import json
import os
from src.config import BENUTZER_DATEN, FOLIEN_DATEN, KURZPRAESENTATION_FOLIEN_DATEN


def lesen_benutzerdaten(db_type='json'):
    if db_type == 'json':
        if os.path.exists(BENUTZER_DATEN):
            with open(BENUTZER_DATEN, 'r', encoding='utf-8') as json_file:
                return json.load(json_file)
        else:
            return {"benutzer": []}
    elif db_type == 'sqlite':
        # user_data = lesen_benutzerdaten('json')
        # set_user_data()
        # return user_data
        raise NotImplementedError('DB type "sqlite" not implemented.')

    else:
        raise NotImplementedError('DB type not implemented.')


def benutzer_speichern(data):
    with open(BENUTZER_DATEN, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)


def get_benutzer_liste():
    return [user for user in lesen_benutzerdaten()['benutzer']]


def lesen_folien_vorlagen():
    if os.path.exists(FOLIEN_DATEN):
        with open(FOLIEN_DATEN, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    else:
        return {"folienvorlagen": []}


def get_folien_vorlagen():
    return [folienvorlage for folienvorlage in lesen_folien_vorlagen()['folienvorlagen']]


# Kurzpräsentation folien
def lesen_kurzpraesentation_folien_json():
    if os.path.exists(KURZPRAESENTATION_FOLIEN_DATEN):
        with open(KURZPRAESENTATION_FOLIEN_DATEN, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    else:
        return {"kurzpraesentation_folien": []}


def kurzpraesentation_folien_speichern(data):
    with open(KURZPRAESENTATION_FOLIEN_DATEN, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)


def get_kurzpraesentation_folien():
    return [user for user in lesen_kurzpraesentation_folien_json()['kurzpraesentation_folien']]


def get_benutzer_kurzpraesentation_folie(user_id):
    return [benutzer_folie for benutzer_folie in lesen_kurzpraesentation_folien_json()['kurzpraesentation_folien'] if
            benutzer_folie['user_id'] == user_id][0] or None


def loeschen_benutzer_kurzpraesentation_daten(user_id):
    kurzpraesentation_folien = lesen_kurzpraesentation_folien_json()
    kurzpraesentation_folien['kurzpraesentation_folien'] = [
        benutzer_folie for benutzer_folie in kurzpraesentation_folien['kurzpraesentation_folien'] if
        benutzer_folie['user_id'] != user_id]
    if kurzpraesentation_folien['kurzpraesentation_folien']:
        kurzpraesentation_folien_speichern(kurzpraesentation_folien)

