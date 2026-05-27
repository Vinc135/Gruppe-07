import json
import os
import datetime


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