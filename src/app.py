import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from src.data.storage import read_data, write_data, get_users
from src.folienvorlage import FolienVorlage
from src.models.user import User
from src.validators import ValidationError, validate_user_data


class NetworkManagerApp(toga.App):
    def __init__(self, formal_name, app_id):
        super().__init__(formal_name=formal_name, app_id=app_id)
        self.data = read_data()

        # user info input
        self.user_id = None
        self.vorname_input = None
        self.nachname_input = None
        self.firmenname_input = None
        self.unternehmensbranche_input = None
        self.telefonnummer_input = None
        self.email_input = None
        self.webseite_input = None
        self.chapter_input = None
        self.mitgliedsstatus_input = None

        # Right container reference
        self.right_container = None

        # template info
        self.folientitel = None
        self.folien_path = None
        self.vortrag_zeit_input = None
        self.naechster_vortrag_input = None

    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name, size=(1050, 700), position=(250, 20))
        self.create_main_layout()
        self.main_window.show()

    def create_input_fields(self, data=None):
        # get id of the user if it is given
        self.user_id = data.get('id', None) if data else None
        # If user data is given, fill the input fields with the data
        self.vorname_input = toga.TextInput(placeholder='Vorname', style=Pack(flex=1, padding=(0, 5)),
                                            value=data.get('vorname', '') if data else '')
        self.nachname_input = toga.TextInput(placeholder='Nachname', style=Pack(flex=1, padding=(0, 5)),
                                             value=data.get('nachname', '') if data else '')
        self.firmenname_input = toga.TextInput(placeholder='Firmenname eingeben', style=Pack(flex=1, padding=(0, 5)),
                                               value=data.get('firmenname', '') if data else '')
        self.unternehmensbranche_input = toga.TextInput(placeholder='Unternehmensbranche eingeben',
                                                        style=Pack(flex=1, padding=(0, 5)),
                                                        value=data.get('unternehmensbranche', '') if data else '')
        self.telefonnummer_input = toga.TextInput(placeholder='Telefonnummer eingeben',
                                                  style=Pack(flex=1, padding=(0, 5)),
                                                  value=data.get('telefonnummer', '') if data else '')
        self.email_input = toga.TextInput(placeholder='E-Mail eingeben', style=Pack(flex=1, padding=(0, 5)),
                                          value=data.get('email', '') if data else '')
        self.webseite_input = toga.TextInput(placeholder='Webseite eingeben', style=Pack(flex=1, padding=(0, 5)),
                                             value=data.get('webseite', '') if data else '')
        self.vortrag_zeit_input = toga.TextInput(placeholder='Präsentationszeit eingeben',
                                                 value=data.get('vortrag_zeit', '20 Sek') if data else "20 Sek",
                                                 style=Pack(flex=1, padding=(0, 5)))
        self.naechster_vortrag_input = toga.TextInput(placeholder='Nächster Vortrag: Vor- und Nachname',
                                                      style=Pack(flex=1, padding=(0, 5)),
                                                      value=data.get('naechster_vortrag', '') if data else '')

        self.chapter_input = toga.Selection(items=['Moin Oldenburg (online)'], style=Pack(flex=1, padding=(0, 5)),
                                            value=data.get('chapter',
                                                           'Moin Oldenburg (online)') if data else 'Moin Oldenburg (online)')
        self.mitgliedsstatus_input = toga.Selection(items=["aktiv", "inaktiv"], style=Pack(flex=1, padding=(0, 5)),
                                                    value=data.get('mitgliedsstatus', 'aktiv') if data else 'aktiv')

    def create_main_layout(self, mitglieder_view=None):
        mitglied_vor_nachname = [(i + 1, f'{value["vorname"]} {value["nachname"]}') for i, value in
                                 enumerate(get_users())]

        left_container = toga.Table(headings=["Nr.", "Mitglieder"], data=mitglied_vor_nachname,
                                    on_select=self.on_mitglied_select, style=Pack(flex=1))

        self.right_container = toga.ScrollContainer(horizontal=False)
        self.right_container.content = toga.Box(style=Pack(direction=COLUMN))

        neues_mitglied_button = toga.Button('Neues Mitglied hinzufügen', on_press=self.mitglied_hinzufuegen,
                                            style=Pack(flex=0, padding=10))

        left_box = toga.Box(children=[neues_mitglied_button, left_container], style=Pack(direction=COLUMN, flex=1))

        split_container = toga.SplitContainer()
        split_container.content = [(left_box, 1), (self.right_container, 2)]

        self.main_window.content = split_container

    def create_right_content(self, is_new_user=False):
        if is_new_user:
            action_button = toga.Button('Speichern', on_press=self.save_data, style=Pack(flex=1, padding=10))
            user_action_button_box = toga.Box(children=[action_button], style=Pack(direction=ROW, padding=10))
        else:
            action_button = toga.Button('Aktualisieren', on_press=self.benutzer_aktualisieren,
                                        style=Pack(flex=1, padding=10))
            delete_user_button = toga.Button('Löschen', on_press=self.delete_user, style=Pack(flex=1, padding=10))
            user_action_button_box = toga.Box(children=[action_button, delete_user_button],
                                              style=Pack(direction=ROW, padding=10))

        vorlage_erzeugen = toga.Button('Kurzpräsentation Vorlage erzeugen', on_press=self.folie_erzeugen,
                                       style=Pack(flex=1, padding=10))
        vortrag_action_button_box = toga.Box(children=[vorlage_erzeugen],
                                             style=Pack(direction=ROW, padding=10))

        label_width = 150
        box = toga.Box(
            children=[
                # Vor- und Nachname
                toga.Box(children=[toga.Label('Vorname:', style=Pack(width=label_width, padding=(5, 5))),
                                   self.vorname_input], style=Pack(direction=ROW, padding=5)),
                toga.Box(children=[toga.Label('Nachname:', style=Pack(width=label_width, padding=(5, 5))),
                                   self.nachname_input], style=Pack(direction=ROW, padding=5)),
                # Firmenname
                toga.Box(children=[toga.Label('Firmenname:', style=Pack(width=label_width, padding=(5, 5))),
                                   self.firmenname_input], style=Pack(direction=ROW, padding=5)),
                # Unternehmensbranche
                toga.Box(children=[toga.Label('Unternehmensbranche:', style=Pack(width=label_width, padding=(5, 5))),
                                   self.unternehmensbranche_input], style=Pack(direction=ROW, padding=5)),
                # Kontaktdaten
                toga.Box(children=[toga.Label('Telefonnummer:', style=Pack(width=label_width, padding=(5, 5))),
                                   self.telefonnummer_input], style=Pack(direction=ROW, padding=5)),
                toga.Box(children=[toga.Label('E-Mail:', style=Pack(width=label_width, padding=(5, 5))),
                                   self.email_input], style=Pack(direction=ROW, padding=5)),
                toga.Box(children=[toga.Label('Webseite:', style=Pack(width=label_width, padding=(5, 5))),
                                   self.webseite_input], style=Pack(direction=ROW, padding=5)),

                toga.Box(children=[toga.Label('Chapter:', style=Pack(width=label_width, padding=(5, 5))),
                                   self.chapter_input], style=Pack(direction=ROW, padding=5)),
                toga.Box(children=[toga.Label('Mitgliedsstatus:', style=Pack(width=label_width, padding=(5, 5))),
                                   self.mitgliedsstatus_input], style=Pack(direction=ROW, padding=5)),

                user_action_button_box,

                toga.Box(children=[
                    toga.Label('Kurzpräsentation Vorlage erzeugen:', style=Pack(width=200, padding=(5, 5)))],
                    style=Pack(direction=ROW, padding=5)),
                toga.Box(children=[toga.Label('Vortragszeit:', style=Pack(width=label_width, padding=(5, 5))),
                                   self.vortrag_zeit_input], style=Pack(direction=ROW, padding=5)),
                toga.Box(children=[toga.Label('Nächster Vortrag:', style=Pack(width=label_width, padding=(5, 5))),
                                   self.naechster_vortrag_input], style=Pack(direction=ROW, padding=5)),
                vortrag_action_button_box
            ],
            style=Pack(direction=COLUMN, padding=10)
        )
        return box

    def on_mitglied_select(self, widget):
        selected_user = widget.selection
        if selected_user is not None:
            users = get_users()
            try:
                selected_vorname, selected_nachname = selected_user.mitglieder.split()
                for user in users:
                    if user['vorname'] == selected_vorname and user['nachname'] == selected_nachname:
                        self.update_right_container(user, is_new_user=False)
                        break
            except AttributeError as e:
                print(f"AttributeError: {e}")

    def update_right_container(self, user, is_new_user=False):
        self.create_input_fields(user)
        box = self.create_right_content(is_new_user=is_new_user)
        self.right_container.content = box

    def mitglied_hinzufuegen(self, widget):
        self.create_input_fields(data={})
        self.update_right_container({}, is_new_user=True)

    def save_data(self, widget):
        user_data = {
            "vorname": self.vorname_input.value,
            "nachname": self.nachname_input.value,
            "firmenname": self.firmenname_input.value,
            "unternehmensbranche": self.unternehmensbranche_input.value,
            "telefonnummer": self.telefonnummer_input.value,
            "email": self.email_input.value,
            "webseite": self.webseite_input.value,
            "chapter": self.chapter_input.value,
            "mitgliedsstatus": self.mitgliedsstatus_input.value
        }

        try:
            # Validate the data
            validate_user_data(user_data)

            # data is valid insert the data into the json file
            user = User(**user_data)

            # Find the highest current id
            if self.data['users']:
                max_id = max(user['id'] for user in self.data['users'])
            else:
                max_id = 0

            # Set the new user's id
            new_user_data = user.to_dict()
            new_user_data['id'] = max_id + 1

            self.data['users'].append(new_user_data)
            write_data(self.data)  # insert user to json file with the storage.py function

            # Refresh the table
            self.create_main_layout()

            self.main_window.info_dialog('Gespeichert!', 'Daten erfolgreich gespeichert!')
        except ValidationError as e:
            self.main_window.error_dialog('Validierungsfehler', str(e))

    def folie_erzeugen(self, widget):
        folienvorlage = read_data()['folienvorlagen'][0]
        user_info = read_data()['users'][0]
        if user_info['vorname'] == "André":
            FolienVorlage(folienvorlage=folienvorlage, user_info=user_info).create_from_template()

    def benutzer_aktualisieren(self, widget):
        user_data = {
            "vorname": self.vorname_input.value,
            "nachname": self.nachname_input.value,
            "firmenname": self.firmenname_input.value,
            "unternehmensbranche": self.unternehmensbranche_input.value,
            "telefonnummer": self.telefonnummer_input.value,
            "email": self.email_input.value,
            "webseite": self.webseite_input.value,
            "chapter": self.chapter_input.value,
            "mitgliedsstatus": self.mitgliedsstatus_input.value
        }

        if self.user_id is not None:
            updated_user = {}
            try:
                validate_user_data(user_data)
                # Find the user and update the information
                for user in self.data['users']:
                    if user['id'] == self.user_id:
                        user['vorname'] = self.vorname_input.value
                        user['nachname'] = self.nachname_input.value
                        user['firmenname'] = self.firmenname_input.value
                        user['unternehmensbranche'] = self.unternehmensbranche_input.value
                        user['telefonnummer'] = self.telefonnummer_input.value
                        user['email'] = self.email_input.value
                        user['webseite'] = self.webseite_input.value
                        user['chapter'] = self.chapter_input.value
                        user['mitgliedsstatus'] = self.mitgliedsstatus_input.value

                        updated_user = user
                        break

                write_data(self.data)  # update the json file

                self.main_window.info_dialog('Aktualisiert!', 'Benutzer erfolgreich aktualisiert!')

                # Refresh the table
                self.create_main_layout()
                # Update the right container with the updated user data
                self.create_input_fields(updated_user)
                self.update_right_container(updated_user, is_new_user=False)
            except ValidationError as e:
                self.main_window.error_dialog('Validierungsfehler', str(e))
            except Exception as e:
                self.main_window.error_dialog('Fehler', str(e))

    async def delete_user(self, widget):
        if self.user_id is not None:
            # Show confirmation dialog
            confirmed = await self.main_window.confirm_dialog(
                'Löschen bestätigen',
                'Möchten Sie diesen Benutzer wirklich löschen?'
            )

            if confirmed:
                try:
                    # Remove the selected user
                    self.data['users'] = [user for user in self.data['users'] if user['id'] != self.user_id]

                    # Update the IDs of the remaining users to be sequential
                    for i, user in enumerate(self.data['users']):
                        user['id'] = i + 1

                    write_data(self.data)  # update the json file

                    await self.main_window.info_dialog('Erfolg', 'Benutzer gelöscht und IDs erfolgreich aktualisiert!')

                    # Refresh the table
                    self.create_main_layout()

                except Exception as e:
                    await self.main_window.error_dialog('Fehler', str(e))
            else:
                await self.main_window.info_dialog('Abgebrochen', 'Benutzerlöschung abgebrochen.')
