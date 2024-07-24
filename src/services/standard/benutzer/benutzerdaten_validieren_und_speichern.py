from src.constants import BENUTZER
from src.models.user import User
from src.data.storage import speichern
from src.services.standard.benutzer.benutzerfoto_speichern import benutzerfoto_speichern
from src.validators import benutzerdaten_validieren


def benutzerdaten_validieren_und_speichern(benutzerdaten, data):
    # Validate the data
    benutzerdaten_validieren(benutzerdaten)

    if benutzerdaten['foto'] != 'Kein Foto ausgewählt':
        benutzerdaten['foto'] = benutzerfoto_speichern(benutzerdaten)
    else:
        benutzerdaten['foto'] = 'resources/images/benutzer/user.png'

    # Data is valid, insert the data into the JSON file
    user = User(**benutzerdaten)

    # Find the highest current id
    if data['benutzer']:
        max_id = max(user['id'] for user in data['benutzer'])
    else:
        max_id = 0

    # Set the new user's id
    new_user_data = user.to_dict()
    new_user_data['id'] = max_id + 1

    data['benutzer'].append(new_user_data)
    speichern(data, model=BENUTZER)
