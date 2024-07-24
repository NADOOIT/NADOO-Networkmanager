import os


def benutzerfoto_loeschen(photo_path):
    if (
            photo_path != 'Kein Foto ausgewählt'
            and photo_path != 'resources/images/benutzer/user.png'
    ):
        try:
            if photo_path and os.path.exists(photo_path):
                os.remove(photo_path)
        except FileNotFoundError:
            print(f"Foto {photo_path} konnte nicht gefunden werden.")
