import curses
import functions
from garage import Garage
from auto import Auto
from auto_validierung import validate_auto_value

# Funktion um ein neues Auto hinzuzufügen
# Die Werte werden über die Konsole einzeln nacheinander eingegeben
def auto_hinzufuegen(stdscr):
    """
    Erfasst ein neues Auto über eine curses-Oberfläche und speichert es in der Garage.

    @param stdscr: curses Screen für die Benutzeroberfläche

    @return: Rückkehr zum Hauptmenü

    @note:
    - Eingaben erfolgen nacheinander für alle Fahrzeugattribute.
    - Pflichtfelder werden geprüft, bei Fehler erfolgt Rücksprung ins Menü.
    - Numerische Werte werden in passende Datentypen umgewandelt.
    """
    try:
        curses.curs_set(1) # setzt curser auf sichtbar
    except curses.error:
        pass
    stdscr.clear()
    content_offset = functions.draw_ascii_header(stdscr)

    fields = [
        ("kennzeichen", "Kennzeichen"),
        ("marke", "Marke"),
        ("modell", "Modell"),
        ("baujahr", "Baujahr"),
        ("kilometer", "Kilometer"),
        ("verbrauch", "Verbrauch"),
        ("tagespreis", "Tagespreis"),
    ]

    inputs = {}
    for i, (key, label) in enumerate(fields): # imput für jede mögliche eingabe eines elements aus fileds
        row = content_offset + i
        functions.safe_addstr(stdscr, row, 0, f"{label}: ") # neue zeile für input unter dem letzten
        stdscr.refresh()
        val = functions.read_limited_input(stdscr, row, len(label) + 2, max_length=40)
        inputs[key] = val # setzt value

    if not (inputs.get("kennzeichen") or "").strip():
        functions.safe_addstr(stdscr, content_offset + len(fields) + 1, 0, "Fehler: Kennzeichen darf nicht leer sein. Drücke eine Taste, um zurückzugehen.")
        stdscr.refresh()
        stdscr.getch()
        return functions.main_menu()

    marke, error = validate_auto_value("marke", inputs.get("marke"))
    if error:
        functions.safe_addstr(stdscr, content_offset + len(fields) + 1, 0, f"Fehler: {error}")
        stdscr.refresh()
        stdscr.getch()
        return functions.main_menu()

    modell, error = validate_auto_value("modell", inputs.get("modell"))
    if error:
        functions.safe_addstr(stdscr, content_offset + len(fields) + 1, 0, f"Fehler: {error}")
        stdscr.refresh()
        stdscr.getch()
        return functions.main_menu()

    baujahr, error = validate_auto_value("baujahr", inputs.get("baujahr"))
    if error:
        functions.safe_addstr(stdscr, content_offset + len(fields) + 1, 0, f"Fehler: {error}")
        stdscr.refresh()
        stdscr.getch()
        return functions.main_menu()

    kilometer = int(inputs.get("kilometer") or 0)

    verbrauch, error = validate_auto_value("verbrauch", inputs.get("verbrauch"))
    if error:
        functions.safe_addstr(stdscr, content_offset + len(fields) + 1, 0, f"Fehler: {error}")
        stdscr.refresh()
        stdscr.getch()
        return functions.main_menu()

    tagespreis, error = validate_auto_value("tagespreis", inputs.get("tagespreis"))
    if error:
        functions.safe_addstr(stdscr, content_offset + len(fields) + 1, 0, f"Fehler: {error}")
        stdscr.refresh()
        stdscr.getch()
        return functions.main_menu()

    auto = Auto(
        inputs.get("kennzeichen"),
        marke,
        modell,
        baujahr,
        kilometer,
        verbrauch,
        tagespreis,
        verliehen=False,
        verliehen_bis=0,
    )

    garage = Garage()
    garage.auto_hinzufügen(auto)

    functions.safe_addstr(stdscr, content_offset + len(fields) + 1, 0, "Auto erfolgreich hinzugefügt. Drücke eine Taste, um zurückzugehen.")
    stdscr.refresh()
    stdscr.getch() # wartet auf userinput

    # Nach dem Hinzufügen zum Menü zurückkehren
    return functions.main_menu()
