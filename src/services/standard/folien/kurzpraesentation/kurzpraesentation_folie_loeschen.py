import os


def kurzpraesentation_folie_loeschen(folien_path):
    if os.path.exists(folien_path):
        os.remove(folien_path)
        print(f"Folie {folien_path} gelöscht.")