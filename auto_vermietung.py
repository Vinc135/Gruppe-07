import curses
import functions
from garage import Garage
from auto import *

# Funktion um ein Auto freizugeben wenn es bereits vermietet ist
def freigeben_screen(stdscr, kennzeichen):
    curses.curs_set(1)
    curses.echo()

    garage = Garage()

    # Auto laden
    auto: Auto = garage.auto_finden(kennzeichen)
    autoname = f"{auto['marke']} {auto['modell']}"

    # Kilometer abfragen
    stdscr.clear()
    content_offset = functions.draw_ascii_header(stdscr)
    stdscr.addstr(content_offset + 0, 0, f"Wie viele Kilometer wurden mit {kennzeichen} gefahren?")
    stdscr.refresh()

    gefahrene_km = int(functions.read_limited_input(stdscr, content_offset + 1, 0, max_length=12).strip())

    # Kilometer addieren
    garage.fahrt_hinzufügen(kennzeichen, gefahrene_km)

    # Auto zurückgeben
    garage.zurueckgeben(kennzeichen)

    curses.noecho()
    curses.curs_set(0)

    # Bestätigungsbildschirm anzeigen
    while True:
        stdscr.clear()
        content_offset = functions.draw_ascii_header(stdscr)
        stdscr.addstr(
            content_offset + 0,
            0,
            f"Das Auto {kennzeichen} {autoname} wurde freigegeben"
        )

        stdscr.addstr(
            content_offset + 2,
            0,
            f"{gefahrene_km} km wurden hinzugefügt."
        )

        stdscr.addstr(content_offset + 4, 0, "Auto erfolgreich freigegeben. Taste drücken")

        key = stdscr.getch()

        if key == curses.KEY_RIGHT:
            return functions.vergebene_autos(stdscr)

        stdscr.refresh()
        stdscr.clear()
        # Nach dem Hinzufügen zum Menü zurückkehren
        return functions.auto_options_menu(stdscr, kennzeichen)

# Funktion kümmert sich um das Vermieten eines Autos bei dem der Nutzer die Details dazu in der Konsole angibt
def vermieten_flow(stdscr, garage, kennzeichen):
    curses.echo()
    stdscr.clear()
    content_offset = functions.draw_ascii_header(stdscr)

    auto = garage.auto_finden(kennzeichen)

    stdscr.addstr(content_offset + 0, 0, "Wie viele Tage vermieten?")
    stdscr.refresh()
    tage = int(functions.read_limited_input(stdscr, content_offset + 1, 0, max_length=6).strip())

    preis = int(auto["tagespreis"]) * tage

    stdscr.addstr(content_offset + 3, 0, f"Endpreis: {preis}€")
    stdscr.addstr(content_offset + 5, 0, "Bestätigen? (j/n): ")
    stdscr.refresh()

    confirm = functions.read_limited_input(stdscr, content_offset + 5, 20, max_length=1).lower()

    curses.noecho()

    if confirm == "j":
        garage.verleihen(kennzeichen, tage)
        stdscr.addstr(content_offset + 7, 0, "Auto erfolgreich vermietet.")
    else:
        stdscr.addstr(content_offset + 7, 0, "Abgebrochen.")

    stdscr.refresh()
    stdscr.clear()
    # Nach dem Hinzufügen zum Menü zurückkehren
    return functions.auto_options_menu(stdscr, kennzeichen)