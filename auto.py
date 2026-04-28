import json
import os

class Auto:
    def __init__(self, id, marke, verbrauch, baujahr, verliehen=False):
        self.id = str(id)
        self.marke = marke
        self.verbrauch = verbrauch
        self.baujahr = baujahr
        self.verliehen = verliehen

    def add_auto(self):
        with open("data.json", "r") as f:
            data = json.load(f)

        data[self.id] = {
            "marke": self.marke,
            "verbrauch": self.verbrauch,
            "baujahr": self.baujahr,
            "verliehen": self.verliehen
        }

        with open("data.json", "w") as f:
            json.dump(data, f, indent=4)

    def load_auto(self):
        with open("data.json", "r") as f:
            data = json.load(f)

        return data.get(self.id)

    def is_verliehen(self):
        auto = self.load_auto()
        return auto["verliehen"] if auto else None
    
    def get_marke(self):
        auto = self.load_auto()
        return auto["marke"] if auto else None

    def get_verbrauch(self):
        auto = self.load_auto()
        return auto["verbrauch"] if auto else None

    def get_baujahr(self):
        auto = self.load_auto()
        return auto["baujahr"] if auto else None
