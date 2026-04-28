import json

class Auto:
    def __init__(self, id, marke, verbrauch, baujahr):
        self.id = id
        self.marke = marke
        self.verbrauch = verbrauch
        self.baujahr = baujahr
    
    def add_auto(self):
        data = {self.id: {self.marke, self.verbrauch, self.baujahr}}
        with open('data.json', 'w') as f:
            json.dump(data, f)
    
    def get_marke(self):
        return self.marke

    def get_verbrauch(self):
        return self.verbrauch

    def get_baujahr(self):
        return self.baujahr