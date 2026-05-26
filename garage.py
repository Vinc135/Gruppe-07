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
        data = self._load()

        if kennzeichen in data:
            del data[kennzeichen]
            self._save(data)
            return True

        return False

    def auto_finden(self, kennzeichen):
        data = self._load()
        return data.get(str(kennzeichen))
    
    def auto_update(self, old_kennzeichen, auto) -> bool:
        data = self._load()
        
        if old_kennzeichen not in data:
            return False
        
        new_kennzeichen = auto["kennzeichen"]
        
        # Wenn das Kennzeichen geändert wurde
        if old_kennzeichen != new_kennzeichen:
            # Prüfe ob neues Kennzeichen bereits existiert
            if new_kennzeichen in data:
                return False
            
            # Lösche alten Eintrag
            del data[old_kennzeichen]
        
        # Erstelle neuen Eintrag (oder aktualisiere bestehenden)
        data[new_kennzeichen] = {
            "marke": auto["marke"],
            "modell": auto["modell"],
            "baujahr": auto["baujahr"],
            "kilometer": auto["kilometer"],
            "verbrauch": auto["verbrauch"],
            "tagespreis": auto["tagespreis"],
            "verliehen": auto.get("verliehen", False),
            "verliehen_bis": auto.get("verliehen_bis", 0)
        }

        self._save(data)
        return True

    def alle_autos(self):
        return self._load()

    def verfügbare_autos(self):
        data = self._load()
        return {k: v for k, v in data.items() if not v["verliehen"]}

    def verliehene_autos(self):
        data = self._load()
        return {k: v for k, v in data.items() if v["verliehen"]}

    def tagesumsatz_berechnen(self):
        data = self._load()
        umsatz = 0

        for auto in data.values():
            if auto["verliehen"]:
                tage = auto.get("verliehen_bis", 0)
                umsatz += auto["tagespreis"] * tage

        return umsatz
