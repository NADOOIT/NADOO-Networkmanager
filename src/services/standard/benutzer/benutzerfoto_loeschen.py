import os


def benutzerfoto_loeschen(photo_path):
    # print(photo_path == 'resources/images/benutzer/user.png')
    if photo_path != 'Kein Foto ausgewählt' and photo_path != 'resources/images/benutzer/user.png':
        if photo_path and os.path.exists(photo_path):
            os.remove(photo_path)