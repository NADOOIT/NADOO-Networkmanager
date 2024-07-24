import toga
from toga.style import Pack
from toga.style.pack import COLUMN

from src.data.storage import lesen_benutzerdaten, get_benutzer_liste, benutzer_speichern, \
    lesen_kurzpraesentation_folien_json, \
    get_folien_vorlagen, kurzpraesentation_folien_speichern, get_benutzer_kurzpraesentation_folie
from src.services import (
    benutzerfoto_loeschen,
    benutzerdaten_validieren_und_speichern,
    benutzerdaten_validieren_und_aktualisieren,
    kurzpraesentation_folie_erzeugen,
    kurzpraesentation_zielpfad_erstellen,
    benutzerdaten_geaendert, kurzpraesentation_folie_loeschen, benutzer_kurzpraesentation_loeschen

)
from src.validators import ValidationError
from src.components.ui.user_input_form import UserForm


class NetworkManagerApp(toga.App):
    def __init__(self, formal_name, app_id):
        super().__init__(formal_name=formal_name, app_id=app_id)
        self.data = lesen_benutzerdaten()
        self.kurzpraesentation_folie_data = lesen_kurzpraesentation_folien_json()
        self.benutzer_folie = None
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
                                 enumerate(get_benutzer_liste())]

        left_container = toga.Table(headings=["ID", "Mitglieder"], data=mitglied_vor_nachname,
                                    on_select=self.on_mitglied_ausgewaehlt, style=Pack(flex=1))

        self.right_container = toga.ScrollContainer(horizontal=False)
        self.right_container.content = toga.Box(style=Pack(direction=COLUMN))

        neues_mitglied_button = toga.Button('Neues Mitglied hinzufügen', on_press=self.neues_mitglied_layout,
                                            style=Pack(flex=0, padding=10))

        left_box = toga.Box(children=[neues_mitglied_button, left_container],
                            style=Pack(direction=COLUMN, flex=1))

        split_container = toga.SplitContainer()
        split_container.content = [(left_box, 1), (self.right_container, 2)]

        self.main_window.content = split_container

    def on_mitglied_ausgewaehlt(self, widget):
        self.is_new_user = False
        selected_row = widget.selection
        if selected_row is not None:
            users = get_benutzer_liste()
            try:
                selected_user_id = selected_row.id
                for user_data in users:
                    if user_data['id'] == selected_user_id:
                        self.is_new_user = False
                        self.selected_user = user_data
                        self.aktualisiere_right_container(user_data, is_new_user=self.is_new_user)
                        break
            except AttributeError as e:
                print(f"AttributeError: {e}")

    def neues_mitglied_layout(self, widget):
        self.is_new_user = True
        self.aktualisiere_right_container({}, is_new_user=self.is_new_user)

    def aktualisiere_right_container(self, user_data, is_new_user=False):
        self.user_form = UserForm(
            benutzer_speichern_callback=self.benutzer_speichern,
            benutzer_aktualisieren_callback=self.benutzer_aktualisieren,
            benutzer_loeschen_callback=self.benutzer_loeschen,
            kurzpraesentation_folie_erzeugen_callback=self.kurzpraesentation_folie_erzeugen,
            is_new_user=is_new_user,
            user_data=user_data,
            user_id=self.selected_user.get('id') if self.selected_user else None,
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
                    benutzerfoto_loeschen(self.selected_user['foto'])  # delete user photo

                    benutzer_kurzpraesentation_loeschen(
                        self.selected_user['id']
                    )  # delete user kurzpraesentation data

                    self.data['benutzer'] = [user for user in self.data['benutzer'] if
                                             user['id'] != self.selected_user['id']]
                    for i, user in enumerate(self.data['benutzer']):
                        user['id'] = i + 1
                    benutzer_speichern(self.data)
                    await self.main_window.info_dialog('Erfolg', 'Benutzer gelöscht und IDs erfolgreich aktualisiert!')
                    self.create_main_layout()
                except Exception as e:
                    await self.main_window.error_dialog('Fehler', str(e))

    async def kurzpraesentation_folie_erzeugen(self, widget):
        benutzer_info_geaendert, benutzerdaten_aus_feldern = benutzerdaten_geaendert(self.user_form, self.selected_user)

        if benutzer_info_geaendert:
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
            else:
                return  # there are not saved data, don't proceed with creating the slide

        # get the all available slide templates
        folienvorlage = get_folien_vorlagen()
        # get the slide template for the kurzpräsentation
        folienvorlage = [vorlage for vorlage in folienvorlage if vorlage['folientitel'] == 'Kurzpräsentation'][0]

        # get the path where the slide should be saved
        dateizielpfad = kurzpraesentation_zielpfad_erstellen(
            user_info=benutzerdaten_aus_feldern,
            folienvorlage=folienvorlage
        )

        try:
            # check if the user already has a slide
            self.benutzer_folie = get_benutzer_kurzpraesentation_folie(user_id=self.selected_user['id'])
        except IndexError:
            self.benutzer_folie = None

        if self.benutzer_folie:
            # The user already has a kurzpräsentation
            for folie in self.kurzpraesentation_folie_data['kurzpraesentation_folien']:
                if folie['user_id'] == self.selected_user['id']:
                    kurzpraesentation_folie_loeschen(folie['folien_path'])  # delete old slide
                    folie['vortragszeit'] = self.user_form.vortrag_zeit_input.value
                    folie['naechster_vortrag'] = self.user_form.naechster_vortrag_input.value or ""
                    folie['folien_path'] = dateizielpfad  # update the path of the slide
                    self.benutzer_folie = folie  # update the user slide data with the new slide data
                    break
        else:
            # The user has no kurzpräsentation slide yet so get input fields values and create a new slide
            kurzpraesentation_folien_data = {
                "user_id": self.selected_user['id'],
                "folientitel": "Kurzpräsentation",
                "vortragszeit": self.user_form.vortrag_zeit_input.value,
                "naechster_vortrag": self.user_form.naechster_vortrag_input.value or "",
                "folien_path": dateizielpfad
            }
            self.benutzer_folie = kurzpraesentation_folien_data  # get the user new slide data
            # append the new slide to the kurzpraesentation_folien.json
            self.kurzpraesentation_folie_data['kurzpraesentation_folien'].append(kurzpraesentation_folien_data)

        # create the kurzpräsentation slide and save it to the kurzpraesentationen folder
        kurzpraesentation_folie_erzeugen(
            folienvorlage=folienvorlage,
            benutzer_folie=self.benutzer_folie,
            user_info=benutzerdaten_aus_feldern
        )

        # write the new kurzpräsentation slide data to the json file
        kurzpraesentation_folien_speichern(self.kurzpraesentation_folie_data)
