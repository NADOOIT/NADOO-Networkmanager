from src.constants import BENUTZER
from src.data.storage import get_data


def get_benutzerdaten():
    return get_data(model=BENUTZER)
