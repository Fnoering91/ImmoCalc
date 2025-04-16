
import json
import os

DATEIPFAD = "immobilien.json"

def lade_immobilien():
    if not os.path.exists(DATEIPFAD):
        return {}
    with open(DATEIPFAD, "r", encoding="utf-8") as f:
        return json.load(f)

def speichere_immobilie(name, daten):
    datenbank = lade_immobilien()
    datenbank[name] = daten
    with open(DATEIPFAD, "w", encoding="utf-8") as f:
        json.dump(datenbank, f, indent=2, ensure_ascii=False)

def loesche_immobilie(name):
    datenbank = lade_immobilien()
    if name in datenbank:
        del datenbank[name]
        with open(DATEIPFAD, "w", encoding="utf-8") as f:
            json.dump(datenbank, f, indent=2, ensure_ascii=False)

def liste_immobilien():
    return list(lade_immobilien().keys())

def lade_immobilie(name):
    return lade_immobilien().get(name, None)
