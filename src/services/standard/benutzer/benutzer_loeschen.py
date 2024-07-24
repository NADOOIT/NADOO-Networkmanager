from src.constants import BENUTZER
from src.data.storage import loeschen


def benutzer_loeschen(data, user_id):
    return loeschen(model=BENUTZER, data=data, user_id=user_id)
