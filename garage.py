import json
import os

from auto import Auto


class Garage:
    FILE = "autos.json"

    def __init__(self):
        if not os.path.exists(self.FILE):
            with open(self.FILE, "w") as f:
                json.dump({}, f)

    def _load(self):
        with open(self.FILE, "r") as f:
            return json.load(f)

    def _save(self, data):
        with open(self.FILE, "w") as f:
            json.dump(data, f, indent=4)

    def auto_hinzufügen(self, auto: Auto):
        """
        Fügt ein neues Auto zur Garage hinzu.

        @param auto: Auto-Objekt

        @return: None
        """
        data = self._load()

        data[auto.kennzeichen] = {
            "marke": auto.marke,
            "modell": auto.modell,
            "baujahr": auto.baujahr,
            "kilometer": auto.kilometer,
            "verbrauch": auto.verbrauch,
            "tagespreis": auto.tagespreis,
            "verliehen": auto.verliehen,
            "verliehen_bis": auto.verliehen_bis
        }

        self._save(data)

    def auto_entfernen(self, kennzeichen):
        """
        Entfernt ein Auto anhand des Kennzeichens.

        @param kennzeichen: Kennzeichen des Autos

        @return: None
        """
        data = self._load()

        if kennzeichen in data:
            del data[kennzeichen]
            self._save(data)

    def auto_finden(self, kennzeichen):
        """
        Sucht ein Auto anhand des Kennzeichens.

        @param kennzeichen: Kennzeichen des Autos

        @return: Dictionary mit Autodaten oder None
        """
        data = self._load()
        return data.get(str(kennzeichen))
    
    def auto_update(self, kennzeichen, auto) -> bool:
        """
        Aktualisiert ein bestehendes Auto.

        @param kennzeichen: Kennzeichen des Autos
        @param auto: Neue Autodaten

        @return: True bei Erfolg, sonst False
        """
        data = self._load()
        
        if kennzeichen not in data:
            return False
        
        data[kennzeichen] = auto

        self._save(data)
        return True

    def alle_autos(self):
        """
        Gibt alle gespeicherten Autos zurück.

        @return: Dictionary aller Autos
        """
        return self._load()

    def verfügbare_autos(self):
        """
        Gibt alle verfügbaren (nicht vermieteten) Autos zurück.

        @return: Gefiltertes Dictionary
        """
        data = self._load()
        return {k: v for k, v in data.items() if not v["verliehen"]}

    def verliehene_autos(self):
        """
        Gibt alle vermieteten Autos zurück.

        @return: Gefiltertes Dictionary
        """
        data = self._load()
        return {k: v for k, v in data.items() if v["verliehen"]}

    def zurueckgeben(self, kennzeichen):
        """
        Gibt ein Auto zurück (beendet Vermietung).

        @param kennzeichen: Kennzeichen des Autos

        @return: True bei Erfolg, sonst False
        """
        data = self._load()
        
        if kennzeichen in data:
            data[kennzeichen]["verliehen"] = False
            data[kennzeichen]["verliehen_bis"] = 0
            self._save(data)
            return True
        
        return False

    def umsatz_berechnen(self):
        """
        Berechnet den erwarteten Gesamtumsatz aus laufenden Vermietungen.

        @return: Gesamtumsatz
        """
        data = self._load()
        umsatz = 0

        for auto in data.values():
            if auto["verliehen"]:
                tage = auto.get("verliehen_bis", 0)
                umsatz += auto["tagespreis"] * tage

        return umsatz

    def verleihen(self, kennzeichen, tage):
        """
        Markiert ein Auto als vermietet.

        @param kennzeichen: Kennzeichen des Autos
        @param tage: Mietdauer in Tagen

        @return: True bei Erfolg, sonst False
        """
        data = self._load()

        auto = data.get(str(kennzeichen))
        if not auto or auto["verliehen"]:
            return False

        auto["verliehen"] = True
        auto["verliehen_bis"] = int(tage)

        data[str(kennzeichen)] = auto
        self._save(data)
        return True

    def fahrt_hinzufügen(self, kennzeichen, kilometer):
        """
        Addiert gefahrene Kilometer zu einem Auto.

        @param kennzeichen: Kennzeichen des Autos
        @param kilometer: Gefahrene Kilometer

        @return: True bei Erfolg
        """
        data = self._load()

        auto = data.get(str(kennzeichen))

        auto["kilometer"] += kilometer

        data[str(kennzeichen)] = auto
        self._save(data)
        return True
