from src.config import BENUTZER_DATEN_FILE, FOLIEN_DATEN_FILE, KURZPRAESENTATION_FOLIEN_DATEN_FILE
from src.constants import BENUTZER, BENUTZER_KURZPRAESENTATION, FOLIEN_VORLAGEN
from src.utils import file_exists, write_to_file, read_file


def get_data(model: str, db_type='json'):
    if db_type == 'json':
        match model:
            case "benutzer":
                if file_exists(BENUTZER_DATEN_FILE):
                    return read_file(BENUTZER_DATEN_FILE)
            case "benutzer_kurzpraesentation":
                if file_exists(KURZPRAESENTATION_FOLIEN_DATEN_FILE):
                    return read_file(KURZPRAESENTATION_FOLIEN_DATEN_FILE)
            case "folienvorlagen":
                if file_exists(FOLIEN_DATEN_FILE):
                    return read_file(FOLIEN_DATEN_FILE)
    else:
        raise NotImplementedError('DB type not implemented.')


def speichern(data, model: str):
    match model:
        case "benutzer":
            write_to_file(BENUTZER_DATEN_FILE, data)
        case "benutzer_kurzpraesentation":
            write_to_file(KURZPRAESENTATION_FOLIEN_DATEN_FILE, data)
        case "folienvorlagen":
            write_to_file(FOLIEN_DATEN_FILE, data)
        case _:
            raise NotImplementedError('Model not implemented.')


def loeschen(model: str, data=None, user_id: int = None):
    match model:
        case "benutzer":
            # create a new list without the user
            data['benutzer'] = [user for user in data['benutzer'] if user['id'] != user_id]
            for i, user in enumerate(data['benutzer']):
                user['id'] = i + 1
            speichern(data, model="benutzer")  # save the new user list to the JSON file
        case "benutzer_kurzpraesentation":
            loeschen_benutzer_kurzpraesentation_daten(user_id)
        case "folienvorlagen":
            # loeschen_folien_vorlagen(data)
            pass
        case _:
            raise NotImplementedError('Model not implemented.')


def get_benutzer_liste():
    return [user for user in get_data(model=BENUTZER)[BENUTZER]]


def get_folien_vorlagen_liste():
    return [folienvorlage for folienvorlage in get_data(model=FOLIEN_VORLAGEN)[FOLIEN_VORLAGEN]]


def get_benutzer_kurzpraesentation_folie(user_id):
    benutzer_folie = [benutzer_folie for benutzer_folie in
                      get_data(model=BENUTZER_KURZPRAESENTATION)[BENUTZER_KURZPRAESENTATION] if
                      benutzer_folie['user_id'] == user_id]
    if benutzer_folie and len(benutzer_folie) > 0:
        return benutzer_folie[0]
    return None


def loeschen_benutzer_kurzpraesentation_daten(user_id):
    kurzpraesentation_folien = get_data(model=BENUTZER_KURZPRAESENTATION)
    # print(kurzpraesentation_folien[BENUTZER_KURZPRAESENTATION])
    kurzpraesentation_folien[BENUTZER_KURZPRAESENTATION] = [
        benutzer_folie for benutzer_folie in kurzpraesentation_folien[BENUTZER_KURZPRAESENTATION] if
        benutzer_folie['user_id'] != user_id]
    speichern(data=kurzpraesentation_folien, model=BENUTZER_KURZPRAESENTATION)
