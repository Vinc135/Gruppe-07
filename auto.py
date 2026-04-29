import json
import os

class Auto:
    FILE = "autos.json"

    def __init__(self, kennzeichen, marke, modell, baujahr, kilometer, verbrauch, tagespreis, verliehen=False, verliehen_bis=0):
        self.kennzeichen = str(kennzeichen)
        self.marke = marke
        self.modell = modell
        self.baujahr = baujahr
        self.kilometer = kilometer
        self.verbrauch = verbrauch
        self.tagespreis = tagespreis
        self.verliehen = verliehen
        self.verliehen_bis = verliehen_bis

    @classmethod
    def _load(cls):
        if os.path.exists(cls.FILE):
            with open(cls.FILE, "r") as f:
                return json.load(f)
        return {}

    @classmethod
    def _save(cls, data):
        with open(cls.FILE, "w") as f:
            json.dump(data, f, indent=4)

    def _refresh(self):
        data = self._load()
        return data.get(self.kennzeichen)

    def verleihen(self, tage):
        data = self._load()
        auto = data.get(self.kennzeichen)

        if not auto or auto["verliehen"]:
            return False

        auto["verliehen"] = True
        auto["verliehen_bis"] = tage
        data[self.kennzeichen] = auto

        self._save(data)
        return True

    def zurückgeben(self):
        data = self._load()
        auto = data.get(self.kennzeichen)

        if not auto:
            return False

        auto["verliehen"] = False
        auto["verliehen_bis"] = 0

        data[self.kennzeichen] = auto
        self._save(data)
        return True

    def is_verfügbar(self):
        auto = self._refresh()
        return auto and not auto["verliehen"]

    def fahrt_hinzufügen(self, kilometer):
        data = self._load()
        auto = data.get(self.kennzeichen)

        if not auto:
            return False

        auto["kilometer"] += kilometer
        data[self.kennzeichen] = auto

        self._save(data)
        return True

    def get_info(self):
        return self._refresh()

    def berechne_mietpreis(self, tage):
        return self.tagespreis * tage
