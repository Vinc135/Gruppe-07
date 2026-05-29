import json
import os
import datetime


class Auto:
    """
    Repräsentiert ein Auto und verwaltet die persistente Speicherung in einer JSON-Datei.

    @attribute FILE: Pfad zur JSON-Datei für die Speicherung aller Autos

    @param kennzeichen: Eindeutiges Kennzeichen des Autos
    @param marke: Hersteller des Autos
    @param modell: Modellbezeichnung
    @param baujahr: Baujahr des Autos
    @param kilometer: Aktueller Kilometerstand
    @param verbrauch: Durchschnittlicher Verbrauch
    @param tagespreis: Mietpreis pro Tag
    @param verliehen: Gibt an, ob das Auto aktuell vermietet ist
    @param verliehen_bis: Datum oder Dauer der aktuellen Vermietung

    @note:
    - Daten werden in einer JSON-Datei gespeichert und geladen.
    - Methoden _load und _save übernehmen das Lesen und Schreiben der Datei.
    - _refresh lädt die aktuellen Daten des Autos anhand des Kennzeichens.
    """
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