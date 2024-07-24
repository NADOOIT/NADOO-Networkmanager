def kurzpraesentation_daten_geaendert(user_form, selected_user) -> (bool, dict):
    kurzpraesentation_daten_aus_feldern = user_form.kurzpraesentation_daten_aus_feldern()
    kurzpraesentation_daten_aus_feldern['id'] = selected_user['id']
