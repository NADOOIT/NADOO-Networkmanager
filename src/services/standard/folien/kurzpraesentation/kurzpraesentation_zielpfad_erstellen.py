import os
from src.utils import ensure_directory_exists


def kurzpraesentation_zielpfad_erstellen(user_info, folienvorlage) -> str:
    """
    Erstellt einen Ordner für die Kurzpräsentationen.
    :return: Pfad zum Ordner
    """
    # Speichere die Änderungen in einer neuen Datei.
    pptx_src_path = folienvorlage['folien_path']
    ordner, dateiname = os.path.split(pptx_src_path)
    name, ext = os.path.splitext(dateiname)
    neuer_dateiname = f"{user_info['vorname']}_kurzpraesentation_user_id_{user_info['id']}{ext}"
    neuer_ordner = os.path.join(ordner, "kurzpraesentationen")
    ensure_directory_exists(neuer_ordner)
    dateizielpfad = os.path.join(neuer_ordner, neuer_dateiname)
    return dateizielpfad.replace('\\', '/')
