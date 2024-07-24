from src.utils import ensure_directory_exists
import os
import shutil
import time


def benutzerfoto_speichern(benutzerdaten):
    photo_path = benutzerdaten['foto']
    if photo_path and photo_path != 'Kein Foto ausgewählt':
        photo_dir = 'resources/images/benutzer'
        ensure_directory_exists(photo_dir)  # Create directory if not exists

        date_string = time.strftime("%Y-%m-%d-%H-%M-%S")

        _, ext = os.path.splitext(photo_path)  # Extract file extension
        photo_filename = f"{benutzerdaten['vorname']}_{date_string}_foto{ext}"
        photo_destination = os.path.join(photo_dir, photo_filename)
        photo_destination = photo_destination.replace('\\', '/')
        if os.path.abspath(photo_path) != os.path.abspath(photo_destination):
            shutil.copy(photo_path, photo_destination)
        return photo_destination
    return photo_path
