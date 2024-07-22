# import toga
# from toga.style import Pack
# from toga.style.pack import COLUMN, ROW
# from src.data.storage import lesen_user_data, benutzer_speichern, get_users, get_folien_vorlagen, \
#     kurzpraesentation_folien_speichern, lesen_kurzpraesentation_folien
# from src.services import (
#     kurzpraesentation_folie_erzeugen,
#     benutzerfoto_loeschen,
#     benutzerdaten_validieren_und_speichern,
#     benutzerdaten_validieren_und_aktualisieren
# )
# from src.validators import ValidationError
#
#
# class NetworkManagerApp(toga.App):
#     def __init__(self, formal_name, app_id):
#         super().__init__(formal_name=formal_name, app_id=app_id)
#         self.data = lesen_user_data()
#         self.kurzpraesentation_folie_data = lesen_kurzpraesentation_folien()
#
#         # check if is a new user or not
#         self.is_new_user = None
#         self.selected_user = None
#
#         # user info input
#         self.user_id = None
#         self.vorname_input = None
#         self.nachname_input = None
#         self.firmenname_input = None
#         self.unternehmensbranche_input = None
#         self.telefonnummer_input = None
#         self.email_input = None
#         self.webseite_input = None
#         self.chapter_input = None
#         self.mitgliedsstatus_input = None
#         self.photo_input = None
#         self.photo_path = None
#
#         # Right container reference
#         self.left_container = None
#         self.right_container = None
#
#         # template info
#         self.folientitel = None
#         self.folien_path = None
#         self.vortrag_zeit_input = None
#         self.naechster_vortrag_input = None
#
#         # buttons
#         self.neues_mitglied_button = None
#         self.action_button = None
#         self.delete_user_button = None
#         self.vorlage_erzeugen_button = None
#
#         # boxes
#         self.user_action_button_box = None
#         self.vortrag_action_button_box = None
#
#     def startup(self):
#         self.main_window = toga.MainWindow(title=self.formal_name, size=(1050, 700), position=(250, 20))
#         self.create_main_layout()
#         self.main_window.show()
#
#     def create_input_fields(self, data=None):
#         # get id of the user if it is given
#         self.user_id = data.get('id', None) if data else None
#         # If user data is given, fill the input fields with the data
#         self.vorname_input = toga.TextInput(placeholder='Vorname', style=Pack(flex=1, padding=(0, 5)),
#                                             value=data.get('vorname', '') if data else '')
#         self.nachname_input = toga.TextInput(placeholder='Nachname', style=Pack(flex=1, padding=(0, 5)),
#                                              value=data.get('nachname', '') if data else '')
#         self.firmenname_input = toga.TextInput(placeholder='Firmenname eingeben', style=Pack(flex=1, padding=(0, 5)),
#                                                value=data.get('firmenname', '') if data else '')
#         self.unternehmensbranche_input = toga.TextInput(placeholder='Unternehmensbranche eingeben',
#                                                         style=Pack(flex=1, padding=(0, 5)),
#                                                         value=data.get('unternehmensbranche', '') if data else '')
#         self.telefonnummer_input = toga.TextInput(placeholder='Telefonnummer eingeben',
#                                                   style=Pack(flex=1, padding=(0, 5)),
#                                                   value=data.get('telefonnummer', '') if data else '')
#         self.email_input = toga.TextInput(placeholder='E-Mail eingeben', style=Pack(flex=1, padding=(0, 5)),
#                                           value=data.get('email', '') if data else '')
#         self.webseite_input = toga.TextInput(placeholder='Webseite eingeben', style=Pack(flex=1, padding=(0, 5)),
#                                              value=data.get('webseite', '') if data else '')
#         self.vortrag_zeit_input = toga.TextInput(placeholder='Präsentationszeit eingeben',
#                                                  value=data.get('vortrag_zeit', '20 Sek') if data else "20 Sek",
#                                                  style=Pack(flex=1, padding=(0, 5)))
#         self.naechster_vortrag_input = toga.TextInput(placeholder='Nächster Vortrag: Vor- und Nachname',
#                                                       style=Pack(flex=1, padding=(0, 5)),
#                                                       value=data.get('naechster_vortrag', '') if data else '')
#
#         self.chapter_input = toga.Selection(items=['Moin Oldenburg (online)'], style=Pack(flex=1, padding=(0, 5)),
#                                             value=data.get(
#                                                 'chapter',
#                                                 'Moin Oldenburg (online)') if data else 'Moin Oldenburg (online)'
#                                             )
#         self.mitgliedsstatus_input = toga.Selection(items=["aktiv", "inaktiv"], style=Pack(flex=1, padding=(0, 5)),
#                                                     value=data.get('mitgliedsstatus', 'aktiv') if data else 'aktiv')
#
#         if self.is_new_user:
#             self.photo_input = toga.Button('Foto auswählen', on_press=self.select_photo,
#                                            style=Pack(flex=1, padding=(0, 5)))
#         else:
#             self.photo_input = toga.Button('Foto ändern', on_press=self.select_photo,
#                                            style=Pack(flex=1, padding=(0, 5)))
#         self.photo_path = toga.Label(text=data.get('foto', 'Kein Foto ausgewählt'),
#                                      style=Pack(flex=1, padding=(0, 5)))  # To display the selected photo path
#
#     def create_main_layout(self):
#         mitglied_vor_nachname = [(i + 1, f'{value["vorname"]} {value["nachname"]}') for i, value in
#                                  enumerate(get_users())]
#
#         self.left_container = toga.Table(headings=["Nr.", "Mitglieder"], data=mitglied_vor_nachname,
#                                          on_select=self.on_mitglied_select, style=Pack(flex=1))
#
#         self.right_container = toga.ScrollContainer(horizontal=False)
#         self.right_container.content = toga.Box(style=Pack(direction=COLUMN))
#
#         self.neues_mitglied_button = toga.Button('Neues Mitglied hinzufügen', on_press=self.mitglied_hinzufuegen,
#                                                  style=Pack(flex=0, padding=10))
#
#         left_box = toga.Box(children=[self.neues_mitglied_button, self.left_container],
#                             style=Pack(direction=COLUMN, flex=1))
#
#         split_container = toga.SplitContainer()
#         split_container.content = [(left_box, 1), (self.right_container, 2)]
#
#         self.main_window.content = split_container
#
#     def create_right_content(self, is_new_user=False):
#         if is_new_user:
#             return self.new_user_box()
#         else:
#             return self.selected_user_box()
#
#     def new_user_box(self):
#         self.action_button = toga.Button('Speichern', on_press=self.benutzer_speichern, style=Pack(flex=1, padding=10))
#         self.user_action_button_box = toga.Box(children=[self.action_button], style=Pack(direction=ROW, padding=10))
#
#         label_width = 150
#         box = toga.Box(
#             children=[
#                 # Vor- und Nachname
#                 toga.Box(children=[toga.Label('Vorname:', style=Pack(width=label_width, padding=(5, 5))),
#                                    self.vorname_input], style=Pack(direction=ROW, padding=5)),
#                 toga.Box(children=[toga.Label('Nachname:', style=Pack(width=label_width, padding=(5, 5))),
#                                    self.nachname_input], style=Pack(direction=ROW, padding=5)),
#                 # Firmenname
#                 toga.Box(children=[toga.Label('Firmenname:', style=Pack(width=label_width, padding=(5, 5))),
#                                    self.firmenname_input], style=Pack(direction=ROW, padding=5)),
#                 # Unternehmensbranche
#                 toga.Box(children=[toga.Label('Unternehmensbranche:', style=Pack(width=label_width, padding=(5, 5))),
#                                    self.unternehmensbranche_input], style=Pack(direction=ROW, padding=5)),
#                 # Kontaktdaten
#                 toga.Box(children=[toga.Label('Telefonnummer:', style=Pack(width=label_width, padding=(5, 5))),
#                                    self.telefonnummer_input], style=Pack(direction=ROW, padding=5)),
#                 toga.Box(children=[toga.Label('E-Mail:', style=Pack(width=label_width, padding=(5, 5))),
#                                    self.email_input], style=Pack(direction=ROW, padding=5)),
#                 toga.Box(children=[toga.Label('Webseite:', style=Pack(width=label_width, padding=(5, 5))),
#                                    self.webseite_input], style=Pack(direction=ROW, padding=5)),
#
#                 toga.Box(children=[toga.Label('Chapter:', style=Pack(width=label_width, padding=(5, 5))),
#                                    self.chapter_input], style=Pack(direction=ROW, padding=5)),
#                 toga.Box(children=[toga.Label('Mitgliedsstatus:', style=Pack(width=label_width, padding=(5, 5))),
#                                    self.mitgliedsstatus_input], style=Pack(direction=ROW, padding=5)),
#                 toga.Box(children=[
#                     toga.Label('Foto:', style=Pack(width=label_width, padding=(5, 5))),
#                     self.photo_input,
#                 ], style=Pack(direction=ROW, padding=5)),
#                 toga.Box(children=[
#                     toga.Label('Foto Pfad:', style=Pack(width=label_width, padding=(5, 5))),
#                     self.photo_path,
#                 ], style=Pack(direction=ROW, padding=5)),
#
#                 self.user_action_button_box
#             ],
#             style=Pack(direction=COLUMN, padding=10)
#         )
#         return box
#
#     def selected_user_box(self):
#         self.action_button = toga.Button('Aktualisieren', on_press=self.benutzer_aktualisieren,
#                                          style=Pack(flex=1, padding=10))
#         self.delete_user_button = toga.Button('Löschen', on_press=self.benutzer_loeschen,
#                                               style=Pack(flex=1, padding=10))
#         self.user_action_button_box = toga.Box(children=[self.action_button, self.delete_user_button],
#                                                style=Pack(direction=ROW, padding=10))
#
#         self.vorlage_erzeugen_button = toga.Button('Kurzpräsentation Vorlage erzeugen',
#                                                    on_press=self.kurzpraesentation_folie_erzeugen,
#                                                    style=Pack(flex=1, padding=10))
#         self.vortrag_action_button_box = toga.Box(children=[self.vorlage_erzeugen_button],
#                                                   style=Pack(direction=ROW, padding=10))
#         label_width = 150
#         box = toga.Box(
#             children=[
#                 # Vor- und Nachname
#                 toga.Box(children=[toga.Label('Vorname:', style=Pack(width=label_width, padding=(5, 5))),
#                                    self.vorname_input], style=Pack(direction=ROW, padding=5)),
#                 toga.Box(children=[toga.Label('Nachname:', style=Pack(width=label_width, padding=(5, 5))),
#                                    self.nachname_input], style=Pack(direction=ROW, padding=5)),
#                 # Firmenname
#                 toga.Box(children=[toga.Label('Firmenname:', style=Pack(width=label_width, padding=(5, 5))),
#                                    self.firmenname_input], style=Pack(direction=ROW, padding=5)),
#                 # Unternehmensbranche
#                 toga.Box(children=[toga.Label('Unternehmensbranche:', style=Pack(width=label_width, padding=(5, 5))),
#                                    self.unternehmensbranche_input], style=Pack(direction=ROW, padding=5)),
#                 # Kontaktdaten
#                 toga.Box(children=[toga.Label('Telefonnummer:', style=Pack(width=label_width, padding=(5, 5))),
#                                    self.telefonnummer_input], style=Pack(direction=ROW, padding=5)),
#                 toga.Box(children=[toga.Label('E-Mail:', style=Pack(width=label_width, padding=(5, 5))),
#                                    self.email_input], style=Pack(direction=ROW, padding=5)),
#                 toga.Box(children=[toga.Label('Webseite:', style=Pack(width=label_width, padding=(5, 5))),
#                                    self.webseite_input], style=Pack(direction=ROW, padding=5)),
#
#                 toga.Box(children=[toga.Label('Chapter:', style=Pack(width=label_width, padding=(5, 5))),
#                                    self.chapter_input], style=Pack(direction=ROW, padding=5)),
#                 toga.Box(children=[toga.Label('Mitgliedsstatus:', style=Pack(width=label_width, padding=(5, 5))),
#                                    self.mitgliedsstatus_input], style=Pack(direction=ROW, padding=5)),
#
#                 toga.Box(children=[
#                     toga.Label('Foto auswählen:', style=Pack(width=label_width, padding=(5, 5))),
#                     self.photo_input,
#                 ], style=Pack(direction=ROW, padding=5)),
#                 toga.Box(children=[
#                     toga.Label('Foto Pfad:', style=Pack(width=label_width, padding=(5, 5))),
#                     self.photo_path,
#                 ], style=Pack(direction=ROW, padding=5)),
#
#                 self.user_action_button_box,
#
#                 toga.Box(children=[
#                     toga.Label('Kurzpräsentation Vorlage erzeugen:', style=Pack(width=200, padding=(5, 5)))],
#                     style=Pack(direction=ROW, padding=5)),
#                 toga.Box(children=[toga.Label('Vortragszeit:', style=Pack(width=label_width, padding=(5, 5))),
#                                    self.vortrag_zeit_input], style=Pack(direction=ROW, padding=5)),
#                 toga.Box(children=[toga.Label('Nächster Vortrag:', style=Pack(width=label_width, padding=(5, 5))),
#                                    self.naechster_vortrag_input], style=Pack(direction=ROW, padding=5)),
#                 self.vortrag_action_button_box
#             ],
#             style=Pack(direction=COLUMN, padding=10)
#         )
#         return box
#
#     async def select_photo(self, widget):
#         try:
#             file_path = await self.main_window.open_file_dialog(title="Foto auswählen", multiple_select=False)
#             if file_path:
#                 self.photo_path.text = str(file_path)
#         except ValueError as e:
#             await self.main_window.error_dialog('Fehler', str(e))
#
#     def on_mitglied_select(self, widget):
#         self.is_new_user = False
#         selected_row = widget.selection
#         if selected_row is not None:
#             users = get_users()
#             try:
#                 selected_vorname, selected_nachname = selected_row.mitglieder.split()
#                 for user in users:
#                     if user['vorname'] == selected_vorname and user['nachname'] == selected_nachname:
#                         self.is_new_user = False
#                         self.selected_user = user
#                         self.update_right_container(user, is_new_user=self.is_new_user)
#                         break
#             except AttributeError as e:
#                 print(f"AttributeError: {e}")
#
#     def update_right_container(self, user, is_new_user=False):
#         self.create_input_fields(user)
#         box = self.create_right_content(is_new_user=is_new_user)
#         self.right_container.content = box
#
#     def mitglied_hinzufuegen(self, widget):
#         self.is_new_user = True
#         self.create_input_fields(data={})
#         self.update_right_container({}, is_new_user=self.is_new_user)
#
#     def benutzerdaten_aus_feldern(self):
#         return {
#             "vorname": self.vorname_input.value,
#             "nachname": self.nachname_input.value,
#             "firmenname": self.firmenname_input.value,
#             "unternehmensbranche": self.unternehmensbranche_input.value,
#             "telefonnummer": self.telefonnummer_input.value,
#             "email": self.email_input.value,
#             "webseite": self.webseite_input.value,
#             "chapter": self.chapter_input.value,
#             "mitgliedsstatus": self.mitgliedsstatus_input.value,
#             "foto": self.photo_path.text
#         }
#
#     def benutzer_speichern(self, widget):
#         user_data = self.benutzerdaten_aus_feldern()
#
#         try:
#             benutzerdaten_validieren_und_speichern(user_data, self.data)
#             # Refresh the table
#             self.create_main_layout()
#             self.main_window.info_dialog('Gespeichert!', 'Daten erfolgreich gespeichert!')
#         except ValidationError as e:
#             self.main_window.error_dialog('Validierungsfehler', str(e))
#
#     def kurzpraesentation_folie_erzeugen(self, widget):
#         if self.is_new_user:
#             self.main_window.error_dialog('Fehler', 'Bitte wählen Sie einen Benutzer aus.')
#         else:
#             folienvorlage = get_folien_vorlagen()
#             folienvorlage = [folienvorlage for folienvorlage in folienvorlage if
#                              folienvorlage['folientitel'] == 'Kurzpräsentation'][0]
#
#             print(self.selected_user['id'])
#
#             dateizielpfad = kurzpraesentation_folie_erzeugen(
#                 folienvorlage=folienvorlage,
#                 user_info=self.selected_user
#             )
#
#             dateizielpfad = dateizielpfad.replace('\\', '/')
#             kurzpraesentation_folien_data = {
#                 "user_id": self.selected_user['id'],
#                 "folientitel": "Kurzpräsentation",
#                 "vortragszeit": self.vortrag_zeit_input.value,
#                 "naechster_vortrag": self.naechster_vortrag_input.value or "Max Mustermann",
#                 "folien_path": dateizielpfad
#             }
#
#             self.kurzpraesentation_folie_data['kurzpraesentation_folien'].append(kurzpraesentation_folien_data)
#
#             kurzpraesentation_folien_speichern(self.kurzpraesentation_folie_data)
#
#     def benutzer_aktualisieren(self, widget):
#         user_data = self.benutzerdaten_aus_feldern()
#
#         if self.user_id is not None:
#             try:
#                 benutzerdaten_validieren_und_aktualisieren(user_data, self.data, self.user_id)
#                 # Refresh the table
#                 self.create_main_layout()
#                 self.main_window.info_dialog('Aktualisiert!', 'Benutzer erfolgreich aktualisiert!')
#                 # Update the right container with the updated user data
#                 self.create_input_fields(user_data)
#                 self.update_right_container(user_data, is_new_user=False)
#             except ValidationError as e:
#                 self.main_window.error_dialog('Validierungsfehler', str(e))
#             except Exception as e:
#                 self.main_window.error_dialog('Fehler', str(e))
#
#     async def benutzer_loeschen(self, widget):
#         if self.user_id is not None:
#             # Show confirmation dialog
#             confirmed = await self.main_window.confirm_dialog(
#                 'Löschen bestätigen',
#                 'Möchten Sie diesen Benutzer wirklich löschen?'
#             )
#
#             if confirmed:
#                 try:
#                     # Find the selected user and their photo path
#                     user_to_delete = None
#                     for user in self.data['benutzer']:
#                         if user['id'] == self.user_id:
#                             user_to_delete = user
#                             break
#
#                     if user_to_delete:
#                         # Delete the user's photo
#                         benutzerfoto_loeschen(user_to_delete)
#
#                         # Remove the selected user
#                         self.data['benutzer'] = [user for user in self.data['benutzer'] if user['id'] != self.user_id]
#
#                         # Update the IDs of the remaining users to be sequential
#                         for i, user in enumerate(self.data['benutzer']):
#                             user['id'] = i + 1
#
#                         benutzer_speichern(self.data)  # update the JSON file
#
#                         await self.main_window.info_dialog('Erfolg',
#                                                            'Benutzer gelöscht und IDs erfolgreich aktualisiert!')
#
#                         # Refresh the table
#                         self.create_main_layout()
#
#                 except Exception as e:
#                     await self.main_window.error_dialog('Fehler', str(e))
#             else:
#                 await self.main_window.info_dialog('Abgebrochen', 'Benutzerlöschung abgebrochen.')
