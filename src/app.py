import os
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from data.models import PresentationSlide, session
from src.slide_template import SlideTemplate
from validators import validate_presentation_data, ValidationError


class NetworkManagerApp(toga.App):
    def __init__(self, formal_name, app_id):
        super().__init__(formal_name=formal_name, app_id=app_id)
        self.folientitel_input = None
        self.firmenname_input = None
        self.unternehmensbranche_input = None
        self.vorname_input = None
        self.nachname_input = None
        self.kontaktdaten_input = None
        self.naechster_vortrag_input = None
        self.vortrag_zeit_input = None

    def startup(self):
        # Create the main window
        self.main_window = toga.MainWindow(title=self.formal_name)

        # Create the input fields
        self.folientitel_input = toga.TextInput(placeholder='Folientitel eingeben', style=Pack(flex=1, padding=(0, 5)))
        self.firmenname_input = toga.TextInput(placeholder='Firmenname eingeben', style=Pack(flex=1, padding=(0, 5)))
        self.unternehmensbranche_input = toga.TextInput(placeholder='Unternehmensbranche eingeben',
                                                        style=Pack(flex=1, padding=(0, 5)))
        self.vortrag_zeit_input = toga.TextInput(placeholder='Präsentationszeit eingeben',
                                                 style=Pack(flex=1, padding=(0, 5)))
        self.vorname_input = toga.TextInput(placeholder='Vorname', style=Pack(flex=1, padding=(0, 5)))
        self.nachname_input = toga.TextInput(placeholder='Nachname', style=Pack(flex=1, padding=(0, 5)))
        self.kontaktdaten_input = toga.MultilineTextInput(placeholder='Kontaktdaten',
                                                          style=Pack(flex=1, padding=(0, 5)))
        self.naechster_vortrag_input = toga.TextInput(placeholder='Nächster Vortrag: Vor- und Nachname',
                                                      style=Pack(flex=1, padding=(0, 5)))

        # Create a button to save the data
        save_button = toga.Button('Speichern', on_press=self.save_data, style=Pack(padding=10))

        update_button = toga.Button('Verarbeiten', on_press=self.update_presentation, style=Pack(padding=10))

        label_width = 150
        # Create labels with some padding for better spacing
        folientitel_label = toga.Label('Folientitel:', style=Pack(width=label_width, padding=(5, 5)))
        firmenname_label = toga.Label('Firmenname:', style=Pack(width=label_width, padding=(5, 5)))
        unternehmensbranche_label = toga.Label('Unternehmensbranche:', style=Pack(width=label_width, padding=(5, 5)))
        vortrag_zeit_label = toga.Label('Vortragszeit:', style=Pack(width=label_width, padding=(5, 5)))
        vorname_label = toga.Label('Vorname:', style=Pack(width=label_width, padding=(5, 5)))
        nachname_label = toga.Label('Nachname:', style=Pack(width=label_width, padding=(5, 5)))
        kontaktdaten_label = toga.Label('Kontaktdaten:', style=Pack(width=label_width, padding=(5, 5)))
        naechster_vortrag_label = toga.Label('Nächster Vortrag:', style=Pack(width=label_width, padding=(5, 5)))

        # Create the main box layout
        box = toga.Box(
            children=[
                # Create a box layout for the input fields and their labels
                toga.Box(children=[folientitel_label, self.folientitel_input], style=Pack(direction=ROW, padding=5)),
                toga.Box(children=[firmenname_label, self.firmenname_input], style=Pack(direction=ROW, padding=5)),
                toga.Box(children=[unternehmensbranche_label, self.unternehmensbranche_input],
                         style=Pack(direction=ROW, padding=5)),
                toga.Box(children=[vortrag_zeit_label, self.vortrag_zeit_input], style=Pack(direction=ROW, padding=5)),
                toga.Box(children=[vorname_label, self.vorname_input], style=Pack(direction=ROW, padding=5)),
                toga.Box(children=[nachname_label, self.nachname_input], style=Pack(direction=ROW, padding=5)),
                toga.Box(children=[kontaktdaten_label, self.kontaktdaten_input], style=Pack(direction=ROW, padding=5)),
                toga.Box(children=[naechster_vortrag_label, self.naechster_vortrag_input],
                         style=Pack(direction=ROW, padding=5)),
                # Add the buttons to the bottom of the box
                save_button,
                update_button
            ],
            # Set the box layout to be a column
            style=Pack(direction=COLUMN, padding=10)
        )

        self.main_window.content = box
        self.main_window.show()

    def save_data(self, widget):
        data = {
            "Folientitel": self.folientitel_input.value,
            "Firmenname": self.firmenname_input.value,
            "Unternehmensbranche": self.unternehmensbranche_input.value,
            "Vorname": self.vorname_input.value,
            "Nachname": self.nachname_input.value,
            "Kontaktdaten": self.kontaktdaten_input.value,
            "Naechster_vortrag": self.naechster_vortrag_input.value,
        }

        try:
            # Validate the data
            validated_data = validate_presentation_data(data)

            # Create a new Presentation instance
            template = PresentationSlide(
                Folientitel=validated_data.Folientitel,
                Firmenname=validated_data.Firmenname,
                Unternehmensbranche=validated_data.Unternehmensbranche,
                Vorname=validated_data.Vorname,
                Nachname=validated_data.Nachname,
                Kontaktdaten=validated_data.Kontaktdaten,
                Naechster_vortrag=validated_data.Naechster_vortrag,
            )

            # Add the input data to the session and commit
            session.add(template)
            session.commit()

            # Provide feedback to the user
            self.main_window.info_dialog('Success', 'Data saved successfully!')

        except ValidationError as e:
            # Provide feedback to the user about validation errors
            self.main_window.error_dialog('Validation Error', str(e))

    def update_presentation(self, widget):
        # Update the PowerPoint slide
        pptx_path = os.path.abspath("resources/ppt_template/Kurzpraesetation-Vorlage.pptx")
        output_path = os.path.abspath(f"resources/ppt_template/Kurzpraesetation-Vorlage-{1}.pptx")
        ppt_updater = SlideTemplate(session, pptx_path)
        ppt_updater.create_from_template(1, output_path)
