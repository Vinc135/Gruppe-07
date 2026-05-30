import curses
import functions
import auto_validierung
from garage import Garage
from auto import Auto


# Funktion um ein bestimmtes Attribut eines Autos zu bearbeiten
# Das Attribut wird über den Parameter "filter" bestimmt
def auto_bearbeiten(stdscr, filter, kennzeichen, auto):
    """
    Bearbeitet ein bestimmtes Attribut eines Autos über eine curses-Oberfläche
    und speichert die Änderung in der Garage.

    @param stdscr: curses Screen für die UI
    @param filter: Zu änderndes Attribut (z. B. "kennzeichen", "marke", "modell", "baujahr", "verbrauch", "tagespreis")
    @param kennzeichen: Aktuelles Kennzeichen (eindeutiger Schlüssel)
    @param auto: Fahrzeugdaten (wird intern neu geladen)

    @return: Rückkehr zum Detailmenü des Autos

    @note:
    - Bei Kennzeichenänderung wird das Auto neu erstellt und das alte gelöscht.
    - Eingaben werden je nach Typ validiert, bei Fehler erfolgt Rücksprung ins Menü.
    """
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
        content_offset = functions.draw_ascii_header(stdscr)
        functions.safe_addstr(stdscr, content_offset + 4, 0, "Error: Es konnte kein gueltiges Attribut gefunden werden.")
        curses.napms(2000)
        return functions.auto_detail_menu(stdscr, kennzeichen)

    stdscr.clear()
    content_offset = functions.draw_ascii_header(stdscr)
    functions.safe_addstr(stdscr, content_offset + 0, 0, f"Bitte waehlen Sie einen neuen Wert fuer {filter}:")
    functions.safe_addstr(stdscr, content_offset + 2, 0, f"Aktueller Wert: {aktueller_wert}")
    functions.safe_addstr(stdscr, content_offset + 4, 0, "Neuer Wert: ")
    try:
        curses.curs_set(1)
    except curses.error:
        pass
    neuer_wert = functions.read_limited_input(stdscr, content_offset + 4, 12, max_length=30).strip()
    try:
        curses.curs_set(0)
    except curses.error:
        pass

    # Fehler schmeissen wenn kein neuer Wert eingegeben wurde
    if neuer_wert == "":
        functions.safe_addstr(stdscr, content_offset + 6, 0, "Fehler: Es wurde kein neuer Wert eingegeben.")
        stdscr.refresh()
        curses.napms(2000)
        return functions.auto_detail_menu(stdscr, kennzeichen)

    error_message = ""
    # Wenn des Kennzeichen geändert wird, muss das Auto gelöscht und mit neuem Kennzeichen wieder hinzugefügt werden, da das Kennzeichen der Key in unserem Dictionary ist
    if filter == "kennzeichen":
        neuer_wert = neuer_wert.upper()
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
    else:
        neuer_wert, error_message = auto_validierung.validiere_auto_wert(filter, neuer_wert, auto)

        if error_message == "":
            auto[filter] = neuer_wert

    # Fehlerbehandlung für fehlgeschlagene Validierung des neuen Werts
    if error_message != "":
        functions.safe_addstr(stdscr, content_offset + 6, 0, f"Fehler: {error_message}")
        stdscr.refresh()
        curses.napms(3000)
        return functions.auto_detail_menu(stdscr, kennzeichen)

    garage = Garage()
    garage.auto_update(kennzeichen, auto)

    if filter == "kennzeichen":
        return functions.auto_detail_menu(stdscr, neuer_wert)

    return functions.auto_detail_menu(stdscr, kennzeichen)