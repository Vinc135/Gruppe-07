import curses
from garage import Garage
from auto import Auto

# Funktion um ein neues Auto hinzuzufügen
# Die Werte werden über die Konsole einzeln nacheinander eingegeben
def auto_hinzufuegen(stdscr):
    curses.curs_set(1) # setzt curser auf sichtbar
    stdscr.clear()

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
        stdscr.addstr(i, 0, f"{label}: ") # neue zeile für input unter dem letzten
        stdscr.refresh()
        curses.echo() # macht eingabe sichtbar
        val = stdscr.getstr(i, len(label) + 2).decode("utf-8") # liest eingabe ein an stelle i der konsole nach dem label +2 für ": "
        curses.noecho() # macht eingabe unsichtbar
        inputs[key] = val # setzt value

    baujahr = int(inputs.get("baujahr") or 0)
    kilometer = int(inputs.get("kilometer") or 0)
    verbrauch = float(inputs.get("verbrauch") or 0)
    tagespreis = float(inputs.get("tagespreis") or 0)

    auto = Auto(
        inputs.get("kennzeichen") or "Kein Kennzeichen angegeben",
        inputs.get("marke") or "Keine Marke gesetzt",
        inputs.get("modell") or "Kein Modell angegeben",
        baujahr,
        kilometer,
        verbrauch,
        tagespreis,
        verliehen=False,
        verliehen_bis=0,
    )

    garage = Garage()
    garage.auto_hinzufügen(auto)

    stdscr.addstr(len(fields) + 1, 0, "Auto erfolgreich hinzugefügt. Drücke eine Taste, um zurückzugehen.")
    stdscr.refresh()
    stdscr.getch() # wartet auf userinput

    # Nach dem Hinzufügen zum Menü zurückkehren
    import functions
    return functions.main_menu()
