from src.models.user import User
from src.data.storage import benutzer_speichern, get_benutzer_liste, get_benutzer_kurzpraesentation_folie, \
    loeschen_benutzer_kurzpraesentation_daten


def benutzerdaten_geaendert(user_form, selected_user) -> (bool, dict):
    benutzerdaten_aus_feldern = user_form.benutzerdaten_aus_feldern()
    benutzerdaten_aus_feldern['id'] = selected_user['id']

    benutzer_info = [user for user in get_benutzer_liste() if user['id'] == selected_user['id']][0]
    # True if the data is different
    return benutzer_info != benutzerdaten_aus_feldern, benutzerdaten_aus_feldern
