import curses
from functions import vergebene_autos
from garage import Garage

# Funktion um ein Auto freizugeben wenn es bereits vermietet ist
def freigeben_screen(stdscr, kennzeichen):
    curses.curs_set(0)
    garage = Garage()
    
    # Auto freigeben und Daten laden
    garage.zurueckgeben(kennzeichen)
    auto = garage.auto_finden(kennzeichen)
    autoname = f"{auto['marke']} {auto['modell']}"
    
    # Bestätigungsbildschirm anzeigen
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, f"Das Auto {kennzeichen} {autoname} wurde freigegeben")
        stdscr.addstr(2, 0, "Auto erfolgreich freigegeben. Taste drücken")
        
        key = stdscr.getch()
        
        if key == curses.KEY_RIGHT:
            return vergebene_autos(stdscr)
        
        stdscr.refresh()

# Funktion kümmert sich um das Vermieten eines Autos bei dem der Nutzer die Details dazu in der Konsole angibt
def vermieten_flow(stdscr, garage, kennzeichen):
    curses.echo()
    stdscr.clear()

    auto = garage.auto_finden(kennzeichen)

    stdscr.addstr(0, 0, "Wie viele Tage vermieten?")
    stdscr.refresh()
    tage = int(stdscr.getstr(1, 0).decode().strip())

    preis = int(auto["tagespreis"]) * tage

    stdscr.addstr(3, 0, f"Endpreis: {preis}€")
    stdscr.addstr(5, 0, "Bestätigen? (j/n): ")
    stdscr.refresh()

    confirm = stdscr.getstr(5, 20).decode().lower()

    curses.noecho()

    if confirm == "j":
        garage.verleihen(kennzeichen, tage)
        stdscr.addstr(7, 0, "Auto erfolgreich vermietet.")
    else:
        stdscr.addstr(7, 0, "Abgebrochen.")

    stdscr.refresh()
    stdscr.getch()