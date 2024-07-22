import os

import toga
from toga.style import Pack
from toga.style.pack import COLUMN

from src.config import KURZPRAESENTATION_FOLIEN_DATEN
from src.data.storage import lesen_user_data, get_benutzer, benutzer_speichern, lesen_kurzpraesentation_folien, \
    get_folien_vorlagen, kurzpraesentation_folien_speichern, get_kurzpraesentation_folien
from src.services import (
    benutzerfoto_loeschen,
    benutzerdaten_validieren_und_speichern,
    benutzerdaten_validieren_und_aktualisieren, kurzpraesentation_folie_erzeugen, kurzpraesentation_zielpfad_erstellen

)
from src.validators import ValidationError
from src.components.ui.user_input_form import UserForm


class NetworkManagerApp(toga.App):
    def __init__(self, formal_name, app_id):
        super().__init__(formal_name=formal_name, app_id=app_id)
        self.data = lesen_user_data()
        self.kurzpraesentation_folie_data = lesen_kurzpraesentation_folien()
        self.is_new_user = None
        self.selected_user = None
        self.user_form = None

        # is used by the update_right_container() method and initialized in the create_main_layout() method
        self.right_container = None

    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name, size=(1050, 700), position=(250, 20))
        self.create_main_layout()
        self.main_window.show()

    def create_main_layout(self):
        mitglied_vor_nachname = [(i + 1, f'{value["vorname"]} {value["nachname"]}') for i, value in
                                 enumerate(get_benutzer())]

        left_container = toga.Table(headings=["Nr.", "Mitglieder"], data=mitglied_vor_nachname,
                                    on_select=self.on_mitglied_ausgewählt, style=Pack(flex=1))

        self.right_container = toga.ScrollContainer(horizontal=False)
        self.right_container.content = toga.Box(style=Pack(direction=COLUMN))

        neues_mitglied_button = toga.Button('Neues Mitglied hinzufügen', on_press=self.mitglied_hinzufuegen,
                                            style=Pack(flex=0, padding=10))

        left_box = toga.Box(children=[neues_mitglied_button, left_container],
                            style=Pack(direction=COLUMN, flex=1))

        split_container = toga.SplitContainer()
        split_container.content = [(left_box, 1), (self.right_container, 2)]

        self.main_window.content = split_container

    def on_mitglied_ausgewählt(self, widget):
        self.is_new_user = False
        selected_row = widget.selection
        if selected_row is not None:
            users = get_benutzer()
            try:
                selected_vorname, selected_nachname = selected_row.mitglieder.split()
                for user in users:
                    if user['vorname'] == selected_vorname and user['nachname'] == selected_nachname:
                        self.is_new_user = False
                        self.selected_user = user
                        self.aktualisiere_right_container(user, is_new_user=self.is_new_user)
                        break
            except AttributeError as e:
                print(f"AttributeError: {e}")

    def mitglied_hinzufuegen(self, widget):
        self.is_new_user = True
        self.aktualisiere_right_container({}, is_new_user=self.is_new_user)

    def aktualisiere_right_container(self, user, is_new_user=False):
        self.user_form = UserForm(
            benutzer_speichern_callback=self.benutzer_speichern,
            benutzer_aktualisieren_callback=self.benutzer_aktualisieren,
            benutzer_loeschen_callback=self.benutzer_loeschen,
            kurzpraesentation_folie_erzeugen_callback=self.kurzpraesentation_folie_erzeugen,
            is_new_user=is_new_user,
            user_data=user
        )
        self.right_container.content = self.user_form.benutzer_layout_erstellen()

    def benutzer_speichern(self, widget):
        user_data = self.user_form.benutzerdaten_aus_feldern()
        try:
            benutzerdaten_validieren_und_speichern(user_data, self.data)
            self.create_main_layout()
            self.main_window.info_dialog('Gespeichert!', 'Daten erfolgreich gespeichert!')
        except ValidationError as e:
            self.main_window.error_dialog('Validierungsfehler', str(e))

    def benutzer_aktualisieren(self, widget):
        user_data = self.user_form.benutzerdaten_aus_feldern()
        if self.selected_user:
            try:
                benutzerdaten_validieren_und_aktualisieren(user_data, self.data, self.selected_user['id'])
                self.create_main_layout()
                self.main_window.info_dialog('Aktualisiert!', 'Benutzer erfolgreich aktualisiert!')
                self.aktualisiere_right_container(user_data, is_new_user=False)
            except ValidationError as e:
                self.main_window.error_dialog('Validierungsfehler', str(e))

    async def benutzer_loeschen(self, widget):
        if self.selected_user:
            confirmed = await self.main_window.confirm_dialog(
                'Löschen bestätigen',
                'Möchten Sie diesen Benutzer wirklich löschen?'
            )
            if confirmed:
                try:
                    benutzerfoto_loeschen(self.selected_user)
                    self.data['benutzer'] = [user for user in self.data['benutzer'] if
                                             user['id'] != self.selected_user['id']]
                    for i, user in enumerate(self.data['benutzer']):
                        user['id'] = i + 1
                    benutzer_speichern(self.data)
                    await self.main_window.info_dialog('Erfolg', 'Benutzer gelöscht und IDs erfolgreich aktualisiert!')
                    self.create_main_layout()
                except Exception as e:
                    await self.main_window.error_dialog('Fehler', str(e))

    import os

    async def kurzpraesentation_folie_erzeugen(self, widget):
        benutzerdaten_aus_feldern = self.user_form.benutzerdaten_aus_feldern()
        benutzerdaten_aus_feldern['id'] = self.selected_user['id']

        user_info = [user for user in get_benutzer() if user['id'] == self.selected_user['id']][0]

        if benutzerdaten_aus_feldern != user_info:
            confirmed = await self.main_window.confirm_dialog(
                'Benutzerdaten geändert',
                'Die Benutzerdaten wurden geändert. Möchten Sie die Änderung speichern before eine neue Folie erstellen?'
            )
            if confirmed:
                self.selected_user['id'] = self.selected_user['id']
                for key, value in benutzerdaten_aus_feldern.items():
                    self.selected_user[key] = value
                # save the changes to the user before creating the slide
                self.benutzer_aktualisieren(self.selected_user)

        folienvorlage = get_folien_vorlagen()
        folienvorlage = [vorlage for vorlage in folienvorlage if vorlage['folientitel'] == 'Kurzpräsentation'][0]

        dateizielpfad = kurzpraesentation_zielpfad_erstellen(
            user_info=benutzerdaten_aus_feldern,
            folienvorlage=folienvorlage
        )

        try:
            benutzer_alte_folie = next(
                (user_folie for user_folie in get_kurzpraesentation_folien() if
                 user_folie['user_id'] == self.selected_user['id']),
                None
            )
        except IndexError:
            benutzer_alte_folie = None

        if benutzer_alte_folie:  # Folie existiert
            for folie in self.kurzpraesentation_folie_data['kurzpraesentation_folien']:
                if folie['user_id'] == self.selected_user['id']:
                    if os.path.exists(folie['folien_path']):
                        os.remove(folie['folien_path'])
                        print(f"Folie {folie['folien_path']} gelöscht.")
                    folie['vortragszeit'] = self.user_form.vortrag_zeit_input.value
                    folie['naechster_vortrag'] = self.user_form.naechster_vortrag_input.value or ""
                    folie['folien_path'] = dateizielpfad
                    break

        else:  # Folie existiert nicht
            kurzpraesentation_folien_data = {
                "user_id": self.selected_user['id'],
                "folientitel": "Kurzpräsentation",
                "vortragszeit": self.user_form.vortrag_zeit_input.value,
                "naechster_vortrag": self.user_form.naechster_vortrag_input.value or "",
                "folien_path": dateizielpfad
            }
            self.kurzpraesentation_folie_data['kurzpraesentation_folien'].append(kurzpraesentation_folien_data)

        kurzpraesentation_folie_erzeugen(
            user_info=benutzerdaten_aus_feldern,
            folienvorlage=folienvorlage

        )

        # Save the new presentation data
        kurzpraesentation_folien_speichern(self.kurzpraesentation_folie_data)
