import curses
import functions
from garage import Garage
from auto import Auto
import datetime


# Funktion um ein bestimmtes Attribut eines Autos zu bearbeiten
# Das Attribut wird über den Parameter "filter" bestimmt
def auto_bearbeiten(stdscr, filter, kennzeichen, auto):
    auto = Garage().auto_finden(kennzeichen)
    aktueller_wert = ""

    if filter == "kennzeichen":
        aktueller_wert = kennzeichen
    elif filter == "marke":
        aktueller_wert = auto["marke"]
    elif filter == "modell":
        aktueller_wert = auto["modell"]
    elif filter == "baujahr":
        aktueller_wert = auto["baujahr"]
    elif filter == "verbrauch":
        aktueller_wert = auto["verbrauch"]
    elif filter == "tagespreis":
        aktueller_wert = auto["tagespreis"]
    else:
        stdscr.clear()
        stdscr.addstr(4, 0, "Error: Es konnte kein gültiges Attribut gefunden werden.")
        curses.napms(2000)
        return functions.auto_detail_menu(stdscr, kennzeichen)

    stdscr.clear()
    stdscr.addstr(0, 0, f"Bitte wählen Sie einen neuen Wert für {filter}:")
    stdscr.addstr(2, 0, f"Aktueller Wert: {aktueller_wert}")
    stdscr.addstr(4, 0, "Neuer Wert: ")
    curses.curs_set(1)
    curses.echo()
    neuer_wert = stdscr.getstr(4, 12, 20).decode("utf-8").strip()
    curses.curs_set(0)
    curses.noecho()

    # Fehler schmeissen wenn kein neuer Wert eingegeben wurde
    if neuer_wert == "":
        stdscr.addstr(6, 0, "Fehler: Es wurde kein neuer Wert eingegeben.")
        stdscr.refresh()
        curses.napms(2000)
        return functions.auto_detail_menu(stdscr, kennzeichen)

    error_message = ""
    # Wenn des Kennzeichen geändert wird, muss das Auto gelöscht und mit neuem Kennzeichen wieder hinzugefügt werden, da das Kennzeichen der Key in unserem Dictionary ist
    if filter == "kennzeichen":
        
        neuer_wert = neuer_wert.strip().upper()
        neuesauto = Auto(
            neuer_wert,
            auto["marke"],
            auto["modell"],
            auto["baujahr"],
            auto["kilometer"],
            auto["verbrauch"],
            auto["tagespreis"],
            auto["verliehen"],
            auto["verliehen_bis"],
        )
        garage = Garage()
        garage.auto_hinzufügen(neuesauto)
        garage.auto_entfernen(kennzeichen)

    # Sonst normale Änderung des Attributs im Auto Dictionary
    elif filter == "marke":
        
        if neuer_wert is None or auto is None or neuer_wert.strip() == "":   
            error_message = "Bitte geben Sie einen gültigen Text ein."
        auto["marke"] = neuer_wert

    elif filter == "modell":
        
        if neuer_wert is None or auto is None or neuer_wert.strip() == "":
            error_message = "Bitte geben Sie einen gültigen Text ein."
        auto["modell"] = neuer_wert

    elif filter == "baujahr":

        try: 
            neuer_wert = int(neuer_wert)
            if neuer_wert is None or auto is None or neuer_wert > datetime.date.today().year or neuer_wert < 1500:
                error_message = "Bitte geben Sie ein Jahr zwischen 1500 und Heute ein."               
            auto["baujahr"] = neuer_wert 
        except ValueError:
            error_message = "Bitte geben Sie ein Jahr zwischen 1500 und Heute ein."
        

    elif filter == "verbrauch":

        try:
            neuer_wert = float(neuer_wert.replace(",", "."))
            if neuer_wert is None or auto is None or neuer_wert < 0:
                error_message = "Bitte geben Sie einen gültigen Gleitkommawert über 0 ein."    
            auto["verbrauch"] = neuer_wert        
        except ValueError:
            error_message = "Bitte geben Sie einen gültigen Gleitkommawert über 0 ein."

    elif filter == "tagespreis":
        
        try:
            neuer_wert = float(neuer_wert.replace(",", "."))
            if neuer_wert is None or auto is None or neuer_wert < 0: 
                error_message = "Bitte geben Sie einen gültigen Gleitkommawert über 0 ein."
            auto["tagespreis"] = neuer_wert
        except ValueError:
            error_message = "Bitte geben Sie einen gültigen Gleitkommawert über 0 ein."

    # Fehlerbehandlung für fehlgeschlagene Validierung des neuen Werts
    if error_message != "":
        stdscr.addstr(6, 0, f"Fehler: {error_message}")
        stdscr.refresh()
        curses.napms(3000)
        return functions.auto_detail_menu(stdscr, kennzeichen)

    garage = Garage()
    garage.auto_update(kennzeichen, auto)

    if filter == "kennzeichen":
        return functions.auto_detail_menu(stdscr, neuer_wert)

    return functions.auto_detail_menu(stdscr, kennzeichen)