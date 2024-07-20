class Folie:
    def __init__(self, folien_path, folientitel, vortragszeit="20 Sek"):
        self.folientitel = folientitel
        self.folien_path = folien_path
        self.vortragszeit = vortragszeit

    def to_dict(self):
        return {
            "folientitel": self.folientitel,
            "folien_path": self.folien_path,
            "vortragszeit": self.vortragszeit,
        }

    @staticmethod
    def from_dict(data):
        return Folie(data['folien_path'], data['folientitel'], data.get('vortragszeit'))
