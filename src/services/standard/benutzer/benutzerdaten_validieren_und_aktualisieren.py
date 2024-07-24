from src.constants import BENUTZER
from src.data.storage import speichern
from src.services.standard.benutzer.benutzerfoto_loeschen import benutzerfoto_loeschen
from src.services.standard.benutzer.benutzerfoto_speichern import benutzerfoto_speichern
from src.validators import benutzerdaten_validieren


def benutzerdaten_validieren_und_aktualisieren(benutzerdaten, data, benutzer_id):
    benutzerdaten_validieren(benutzerdaten)

    if benutzerdaten['foto'] != 'Kein Foto ausgewählt':
        benutzerdaten['foto'] = benutzerfoto_speichern(benutzerdaten)
    elif (
            benutzerdaten['foto'] == 'Kein Foto ausgewählt'
            or benutzerdaten['foto'] == ''
            or not benutzerdaten['foto']
    ):
        benutzerdaten['foto'] = 'resources/images/benutzer/user.png'

    # Find the user and update the information
    for benutzer in data['benutzer']:
        if benutzer['id'] == benutzer_id:
            benutzer['vorname'] = benutzerdaten['vorname']
            benutzer['nachname'] = benutzerdaten['nachname']
            benutzer['firmenname'] = benutzerdaten['firmenname']
            benutzer['unternehmensbranche'] = benutzerdaten['unternehmensbranche']
            benutzer['telefonnummer'] = benutzerdaten['telefonnummer']
            benutzer['email'] = benutzerdaten['email']
            benutzer['webseite'] = benutzerdaten['webseite']
            benutzer['chapter'] = benutzerdaten['chapter']
            benutzer['mitgliedsstatus'] = benutzerdaten['mitgliedsstatus']
            if benutzerdaten['foto'] != 'Kein Foto ausgewählt':
                benutzerfoto_loeschen(benutzer['foto'])  # Delete old photo
                benutzer['foto'] = benutzerdaten['foto']
            break

    speichern(data, model=BENUTZER)
