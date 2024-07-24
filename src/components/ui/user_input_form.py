import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from src.data.storage import get_benutzer_kurzpraesentation_folie


class UserForm:
    def __init__(self,
                 benutzer_speichern_callback,
                 benutzer_aktualisieren_callback,
                 benutzer_loeschen_callback,
                 kurzpraesentation_folie_erzeugen_callback,
                 is_new_user,
                 user_data=None,
                 user_id=None,
                 ):

        self.is_new_user = is_new_user
        self.user_data = user_data or {}
        self.benutzer_folie = {}

        if not self.is_new_user:
            self.user_data['id'] = user_id

        if self.user_data:
            try:
                # check if the user already has a slide
                self.benutzer_folie = get_benutzer_kurzpraesentation_folie(user_id=self.user_data['id'])
            except IndexError:
                self.benutzer_folie = {}

        # function from src\app.py
        self.benutzer_speichern = benutzer_speichern_callback
        self.benutzer_aktualisieren = benutzer_aktualisieren_callback
        self.benutzer_loeschen = benutzer_loeschen_callback
        self.kurzpraesentation_folie_erzeugen = kurzpraesentation_folie_erzeugen_callback

        # Initialize input fields and buttons
        self.eingabe_felder_erstellen()
        self.knoepfe_erstellen()

    def eingabe_felder_erstellen(self):
        self.user_id = self.user_data.get('id', None)
        self.vorname_input = toga.TextInput(placeholder='Vorname', style=Pack(flex=1, padding=(0, 5)),
                                            value=self.user_data.get('vorname', ''))
        self.nachname_input = toga.TextInput(placeholder='Nachname', style=Pack(flex=1, padding=(0, 5)),
                                             value=self.user_data.get('nachname', ''))
        self.firmenname_input = toga.TextInput(placeholder='Firmenname eingeben', style=Pack(flex=1, padding=(0, 5)),
                                               value=self.user_data.get('firmenname', ''))
        self.unternehmensbranche_input = toga.TextInput(placeholder='Unternehmensbranche eingeben',
                                                        style=Pack(flex=1, padding=(0, 5)),
                                                        value=self.user_data.get('unternehmensbranche', ''))
        self.telefonnummer_input = toga.TextInput(placeholder='Telefonnummer eingeben',
                                                  style=Pack(flex=1, padding=(0, 5)),
                                                  value=self.user_data.get('telefonnummer', ''))
        self.email_input = toga.TextInput(placeholder='E-Mail eingeben', style=Pack(flex=1, padding=(0, 5)),
                                          value=self.user_data.get('email', ''))
        self.webseite_input = toga.TextInput(placeholder='Webseite eingeben', style=Pack(flex=1, padding=(0, 5)),
                                             value=self.user_data.get('webseite', ''))
        self.chapter_input = toga.Selection(items=['Moin Oldenburg (online)'], style=Pack(flex=1, padding=(0, 5)),
                                            value=self.user_data.get('chapter', 'Moin Oldenburg (online)'))
        self.mitgliedsstatus_input = toga.Selection(items=["aktiv", "inaktiv"], style=Pack(flex=1, padding=(0, 5)),
                                                    value=self.user_data.get('mitgliedsstatus', 'aktiv'))
        self.photo_input = toga.Button('Foto auswählen' if self.is_new_user else 'Foto ändern',
                                       on_press=self.benutzer_foto_auswaehlen,
                                       style=Pack(flex=1, padding=(0, 5)))
        self.photo_path = toga.Label(text=self.user_data.get('foto', 'Kein Foto ausgewählt'),
                                     style=Pack(flex=1, padding=(0, 5)))  # To display the selected photo path

        # Additional input fields for presentation
        self.vortrag_zeit_input = toga.TextInput(placeholder='Präsentationszeit eingeben',
                                                 value=self.benutzer_folie.get('vortragszeit', '') if self.user_data else "20 Sek",
                                                 style=Pack(flex=1, padding=(0, 5)))
        self.naechster_vortrag_input = toga.TextInput(placeholder='Nächster Vortrag: Vor- und Nachname',
                                                      style=Pack(flex=1, padding=(0, 5)),
                                                      value=self.benutzer_folie.get('naechster_vortrag', '') if self.user_data else '')

    def knoepfe_erstellen(self):
        if self.is_new_user:
            self.action_buttons_box = toga.Box(
                children=[
                    toga.Button(
                        'Speichern',
                        on_press=self.benutzer_speichern,
                        style=Pack(flex=1, padding=10)  # Set flex to 1
                    )], style=Pack(direction=ROW, flex=1, padding=5))
        else:
            self.action_buttons_box = toga.Box(
                children=[
                    toga.Button(
                        'Änderungen speichern',
                        on_press=self.benutzer_aktualisieren,
                        style=Pack(flex=1, padding=10)  # Set flex to 1
                    ),
                    toga.Button(
                        'Löschen',
                        on_press=self.benutzer_loeschen,
                        style=Pack(flex=1, padding=10)  # Set flex to 1
                    )], style=Pack(direction=ROW, flex=1, padding=5))

            self.vorlage_erzeugen_button = toga.Button('Kurzpräsentation Vorlage erzeugen',
                                                       on_press=self.kurzpraesentation_folie_erzeugen,
                                                       style=Pack(flex=1, padding=10))
            self.vortrag_action_button_box = toga.Box(children=[self.vorlage_erzeugen_button],
                                                      style=Pack(direction=ROW, padding=10))

    def benutzer_layout_erstellen(self):
        label_width = 150
        form_box = toga.Box(
            children=[
                toga.Box(children=[toga.Label('Vorname:', style=Pack(width=label_width, padding=(5, 5))),
                                   self.vorname_input], style=Pack(direction=ROW, padding=5)),
                toga.Box(children=[toga.Label('Nachname:', style=Pack(width=label_width, padding=(5, 5))),
                                   self.nachname_input], style=Pack(direction=ROW, padding=5)),
                toga.Box(children=[toga.Label('Firmenname:', style=Pack(width=label_width, padding=(5, 5))),
                                   self.firmenname_input], style=Pack(direction=ROW, padding=5)),
                toga.Box(children=[toga.Label('Unternehmensbranche:', style=Pack(width=label_width, padding=(5, 5))),
                                   self.unternehmensbranche_input], style=Pack(direction=ROW, padding=5)),
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
                toga.Box(children=[toga.Label('Foto:', style=Pack(width=label_width, padding=(5, 5))),
                                   self.photo_input], style=Pack(direction=ROW, padding=5)),
                toga.Box(children=[toga.Label('Foto Pfad:', style=Pack(width=label_width, padding=(5, 5))),
                                   self.photo_path], style=Pack(direction=ROW, padding=5)),
                self.action_buttons_box
            ],
            style=Pack(direction=COLUMN, padding=10)
        )

        # Only add the presentation fields if it's NOT a new user adding case
        if not self.is_new_user:
            form_box.add(
                toga.Box(
                    children=[
                        toga.Label('Kurzpräsentation Vorlage erzeugen:', style=Pack(width=200, padding=(5, 5)))
                    ],
                    style=Pack(direction=ROW, padding=5)
                )
            )
            form_box.add(
                toga.Box(
                    children=[toga.Label('Vortragszeit:', style=Pack(width=label_width, padding=(5, 5))),
                              self.vortrag_zeit_input],
                    style=Pack(direction=ROW, padding=5)
                )
            )
            form_box.add(
                toga.Box(
                    children=[toga.Label('Nächster Vortrag:', style=Pack(width=label_width, padding=(5, 5))),
                              self.naechster_vortrag_input],
                    style=Pack(direction=ROW, padding=5)
                )
            )
            form_box.add(self.vortrag_action_button_box)

        return form_box

    def benutzerdaten_aus_feldern(self):
        return {
            "vorname": self.vorname_input.value,
            "nachname": self.nachname_input.value,
            "firmenname": self.firmenname_input.value,
            "unternehmensbranche": self.unternehmensbranche_input.value,
            "telefonnummer": self.telefonnummer_input.value,
            "email": self.email_input.value,
            "webseite": self.webseite_input.value,
            "chapter": self.chapter_input.value,
            "mitgliedsstatus": self.mitgliedsstatus_input.value,
            "foto": self.photo_path.text,
        }

    async def benutzer_foto_auswaehlen(self, widget):
        try:
            file_path = await widget.window.open_file_dialog(title="Foto auswählen", multiple_select=False)
            if file_path:
                self.photo_path.text = str(file_path)
        except ValueError as e:
            await widget.window.error_dialog('Fehler', str(e))
