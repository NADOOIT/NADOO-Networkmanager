from dataclasses import dataclass


@dataclass
class User:
    def __init__(self, vorname, nachname, firmenname, unternehmensbranche, telefonnummer, email, webseite, chapter,
                 mitgliedsstatus, foto=None):
        self.vorname = vorname
        self.nachname = nachname
        self.firmenname = firmenname
        self.unternehmensbranche = unternehmensbranche
        self.telefonnummer = telefonnummer
        self.email = email
        self.webseite = webseite
        self.chapter = chapter
        self.mitgliedsstatus = mitgliedsstatus
        self.foto = foto

    def to_dict(self):
        return {
            "vorname": self.vorname,
            "nachname": self.nachname,
            "firmenname": self.firmenname,
            "unternehmensbranche": self.unternehmensbranche,
            "telefonnummer": self.telefonnummer,
            "email": self.email,
            "webseite": self.webseite,
            "chapter": self.chapter,
            "mitgliedsstatus": self.mitgliedsstatus,
            "foto": self.foto
        }

    @staticmethod
    def from_dict(data):
        return User(data.get('vorname'), data.get('nachname'), data.get('firmenname'), data.get('unternehmensbranche'),
                    data.get('telefonnummer'), data.get('email'), data.get('webseite'), data.get('chapter'),
                    data.get('mitgliedsstatus'), data.get('foto'))
