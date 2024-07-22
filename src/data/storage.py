import json
import os
from src.config import BENUTZER_DATEN, FOLIEN_DATEN, KURZPRAESENTATION_FOLIEN_DATEN


def lesen_user_data():
    if os.path.exists(BENUTZER_DATEN):
        with open(BENUTZER_DATEN, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    else:
        return {"benutzer": []}


def benutzer_speichern(data):
    with open(BENUTZER_DATEN, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)


def get_benutzer():
    return [user for user in lesen_user_data()['benutzer']]


def lesen_folien_vorlagen():
    if os.path.exists(FOLIEN_DATEN):
        with open(FOLIEN_DATEN, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    else:
        return {"folienvorlagen": []}


def get_folien_vorlagen():
    return [folienvorlage for folienvorlage in lesen_folien_vorlagen()['folienvorlagen']]


# Kurzpräsentation folien
def lesen_kurzpraesentation_folien():
    if os.path.exists(KURZPRAESENTATION_FOLIEN_DATEN):
        with open(KURZPRAESENTATION_FOLIEN_DATEN, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    else:
        return {"kurzpraesentation_folien": []}


def kurzpraesentation_folien_speichern(data):
    with open(KURZPRAESENTATION_FOLIEN_DATEN, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)


def get_kurzpraesentation_folien():
    return [user for user in lesen_kurzpraesentation_folien()['kurzpraesentation_folien']]


def delete_element(data, element_id):
    pass
