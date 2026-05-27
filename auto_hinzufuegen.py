import curses
import functions
from garage import Garage
from auto import Auto

# Funktion um ein neues Auto hinzuzufügen
# Die Werte werden über die Konsole einzeln nacheinander eingegeben
def auto_hinzufuegen(stdscr):
    curses.curs_set(1) # setzt curser auf sichtbar
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
        stdscr.addstr(row, 0, f"{label}: ") # neue zeile für input unter dem letzten
        stdscr.refresh()
        val = functions.read_limited_input(stdscr, row, len(label) + 2, max_length=40)
        inputs[key] = val # setzt value

    if not (inputs.get("kennzeichen") or "").strip():
        stdscr.addstr(content_offset + len(fields) + 1, 0, "Fehler: Kennzeichen darf nicht leer sein. Drücke eine Taste, um zurückzugehen.")
        stdscr.refresh()
        stdscr.getch()
        return functions.main_menu()

    if not (inputs.get("marke") or "").strip():
        stdscr.addstr(content_offset + len(fields) + 1, 0, "Fehler: Marke darf nicht leer sein. Drücke eine Taste, um zurückzugehen.")
        stdscr.refresh()
        stdscr.getch()
        return functions.main_menu()

    if not (inputs.get("modell") or "").strip():
        stdscr.addstr(content_offset + len(fields) + 1, 0, "Fehler: Modell darf nicht leer sein. Drücke eine Taste, um zurückzugehen.")
        stdscr.refresh()
        stdscr.getch()
        return functions.main_menu()

    baujahr_raw = (inputs.get("baujahr") or "").strip()
    if not baujahr_raw:
        stdscr.addstr(content_offset + len(fields) + 1, 0, "Fehler: Kein Baujahr angegeben. Drücke eine Taste, um zurückzugehen.")
        stdscr.refresh()
        stdscr.getch()
        return functions.main_menu()
    baujahr = int(baujahr_raw)

    kilometer = int(inputs.get("kilometer") or 0)

    verbrauch_raw = (inputs.get("verbrauch") or "").strip()
    if not verbrauch_raw:
        stdscr.addstr(content_offset + len(fields) + 1, 0, "Fehler: Kein Verbrauch angegeben. Drücke eine Taste, um zurückzugehen.")
        stdscr.refresh()
        stdscr.getch()
        return functions.main_menu()
    verbrauch = float(verbrauch_raw)

    tagespreis_raw = (inputs.get("tagespreis") or "").strip()
    if not tagespreis_raw:
        stdscr.addstr(content_offset + len(fields) + 1, 0, "Fehler: Kein Tagespreis angegeben. Drücke eine Taste, um zurückzugehen.")
        stdscr.refresh()
        stdscr.getch()
        return functions.main_menu()
    tagespreis = float(tagespreis_raw)

    auto = Auto(
        inputs.get("kennzeichen"),
        inputs.get("marke"),
        inputs.get("modell"),
        baujahr,
        kilometer,
        verbrauch,
        tagespreis,
        verliehen=False,
        verliehen_bis=0,
    )

    garage = Garage()
    garage.auto_hinzufügen(auto)

    stdscr.addstr(content_offset + len(fields) + 1, 0, "Auto erfolgreich hinzugefügt. Drücke eine Taste, um zurückzugehen.")
    stdscr.refresh()
    stdscr.getch() # wartet auf userinput

    # Nach dem Hinzufügen zum Menü zurückkehren
    return functions.main_menu()
