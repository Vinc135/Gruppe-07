import curses
from auto_vermietung import *
from garage import Garage 
from auto_hinzufuegen import auto_hinzufuegen
from auto_bearbeiten import auto_bearbeiten

ASCII_HEADER = [
    r"+------------------------------------------------------------+",
    r"|                      AUTO VERMIETUNG                       |",
    r"+------------------------------------------------------------+",
]


def safe_addstr(stdscr, row, col, text, attr=None):
    """
    Gibt Text sicher auf dem Bildschirm aus und verhindert Überläufe.

    @param stdscr: curses Screen
    @param row: Zeile für die Ausgabe
    @param col: Spalte für die Ausgabe
    @param text: Auszugebender Text
    @param attr: Optionales Attribut (z. B. Hervorhebung)

    @return: None
    """
    max_y, max_x = stdscr.getmaxyx()

    if row < 0 or row >= max_y or col >= max_x:
        return

    safe_col = max(col, 0)
    text_value = str(text)

    if col < 0:
        text_value = text_value[-col:]

    available_width = max_x - safe_col - 1
    if available_width <= 0:
        return

    clipped_text = text_value[:available_width]
    if not clipped_text:
        return

    try:
        if attr is None:
            stdscr.addstr(row, safe_col, clipped_text)
        else:
            stdscr.addstr(row, safe_col, clipped_text, attr)
    except curses.error:
        pass


def draw_ascii_header(stdscr):
    """
    Zeichnet den ASCII-Header und gibt den Offset für den Inhalt zurück.

    @param stdscr: curses Screen

    @return: Startzeile für weiteren Inhalt
    """
    max_y, max_x = stdscr.getmaxyx()

    for row, line in enumerate(ASCII_HEADER):
        if row >= max_y:
            break

        clipped_line = line[: max_x - 1] if max_x > 1 else ""
        safe_addstr(stdscr, row, 0, clipped_line)

    # One empty spacer line between header and menu content.
    return min(len(ASCII_HEADER) + 1, max_y)


def read_limited_input(stdscr, row, col, max_length=30):
    """
    Liest eine Benutzereingabe mit begrenzter Länge ein.

    @param stdscr: curses Screen
    @param row: Zeile der Eingabe
    @param col: Spalte der Eingabe
    @param max_length: Maximale Länge der Eingabe

    @return: Eingegebener String
    """
    max_y, max_x = stdscr.getmaxyx()

    if row >= max_y:
        return ""

    available_width = max_x - col - 1
    if available_width <= 0:
        return ""

    read_limit = min(max_length, available_width)

    curses.echo()
    value = stdscr.getstr(row, col, read_limit).decode("utf-8")
    curses.noecho()
    return value

def draw_menu(stdscr):
    """
    Initialisiert das Hauptmenü und startet die Navigation.

    @param stdscr: curses Screen

    @return: None
    """
    try:
        curses.curs_set(0)  # Hide the cursor
    except curses.error:
        pass

    menu_options, action_map, title = main_menu()
    exit_loop = False
    while True:
        menu_options, action_map, title = handle_user_input(
            stdscr,
            menu_options,
            0,
            "",
            action_map,
            title,
        )

        if exit_loop:
            break


################################################################################

def handle_user_input(
    stdscr,
    menu_options,
    current_row,
    key_input,
    action_map,
    title=None,
    prompt="Navigiere mit den Pfeiltasten und drücke die rechte Pfeiltaste, um eine Auswahl zu treffen: ",
):
    """
    Verarbeitet Benutzereingaben und steuert die Menü-Navigation.

    @param stdscr: curses Screen
    @param menu_options: Liste der Menüeinträge
    @param current_row: Aktuell ausgewählte Zeile
    @param key_input: Zwischenspeicher für Zahleneingaben
    @param action_map: Mapping von Auswahl zu Funktionen
    @param title: Optionaler Titel des Menüs
    @param prompt: Hinweistext für die Bedienung

    @return: Tupel aus Menüoptionen, Action-Map und Titel
    """
    while True:
        stdscr.clear()
        content_offset = draw_ascii_header(stdscr)
        max_y, max_x = stdscr.getmaxyx()

        if title:
            safe_addstr(stdscr, content_offset, 0, title)
            title_offset = 1
        else:
            title_offset = 0

        required_rows = content_offset + title_offset + len(menu_options) + 4
        required_cols = max(
            len(prompt) + 1,
            len(title or "") + 1,
            *(len(option) + 3 for option in menu_options),
        )

        if max_y <= required_rows or max_x <= required_cols:
            stdscr.clear()
            content_offset = draw_ascii_header(stdscr)
            safe_addstr(stdscr, content_offset + 0, 0, "Fenster zu klein für die aktuelle Ansicht.")
            safe_addstr(stdscr, content_offset + 1, 0, "Bitte Terminal vergrößern und eine Taste drücken.")
            stdscr.refresh()
            stdscr.getch()
            continue

        # Menu starts from line 1 (or 0 if no title)
        for idx, row in enumerate(menu_options):
            if idx == current_row:
                safe_addstr(stdscr, idx + content_offset + title_offset + 1, 0, f"> {row}", curses.A_REVERSE)
            else:
                safe_addstr(stdscr, idx + content_offset + title_offset + 1, 0, f"  {row}")

        safe_addstr(stdscr, len(menu_options) + content_offset + title_offset + 2, 0, prompt)

        key = stdscr.getch()  # Get user input

        if key == curses.KEY_UP:  # If the UP arrow key is pressed
            current_row = (current_row - 1) % len(menu_options)  # Wrap around using modulo
        elif key == curses.KEY_DOWN:  # If the DOWN arrow key is pressed
            current_row = (current_row + 1) % len(menu_options)  # Wrap around using modulo
        elif key == curses.KEY_RIGHT:  # If the RIGHT arrow key is pressed
            if current_row in action_map:

                a, b, c = action_map[current_row](stdscr)
                return a, b, c
        else:
            try:
                number = int(key) - 48  # Convert the key to a number by subtracting ASCII value of '0'
                if 0 <= number <= 9:  # Check if the number is valid
                    old_keyinput = key_input  # Store the old key input
                    key_input += str(number)  # Append the number to key input
                    if (
                        int(key_input) <= len(menu_options) - 1
                    ):  # Check if the new concatenated number is in the menu range
                        current_row = int(key_input)  # Update current row
                    elif number <= len(menu_options) - 1:  # Check if the single number is within the menu range
                        key_input = str(number)
                        current_row = number
                    else:
                        key_input = str(old_keyinput)
                        if key_input != "":
                            current_row = int(key_input)
            except ValueError:
                safe_addstr(
                    len(menu_options) + content_offset + title_offset + 3,
                    0,
                    "Ungültige Eingabe, bitte versuche es erneut.",
                )
                stdscr.refresh()
                curses.napms(1000)  # Wait 1 second before redrawing the menu

        stdscr.refresh()

## Main Menu (Ausgangsmenü) #####################################################################
def main_menu():
    """
    Erstellt das Hauptmenü mit allen verfügbaren Aktionen.

    @return: Tupel aus Menüoptionen, Action-Map und Titel
    """
    menu_options = [
        "(0) Auto hinzufügen",
        "(1) Alle Autos anzeigen",
        "(2) Freie Autos anzeigen",
        "(3) Vermietete Autos anzeigen",
        "(4) Erwarteter Umsatz berechnen"
    ]

    action_map = {
        0: lambda stdscr: auto_hinzufuegen(stdscr),
        1: lambda stdscr: autos_anzeigen(stdscr),
        2: lambda stdscr: freie_autos(stdscr),
        3: lambda stdscr: vergebene_autos(stdscr),
        4: lambda stdscr: umsatz(stdscr)
    }

    return menu_options, action_map, "Hauptmenü"

############ Filter Typen

def autos_anzeigen(stdscr):
    """
    Zeigt alle Autos an.

    @param stdscr: curses Screen

    @return: Weiterleitung zum Listenmenü
    """
    return auto_liste_menu(stdscr, filter_type="alle", title="Alle Autos")

def freie_autos(stdscr):
    """
    Zeigt alle freien (nicht vermieteten) Autos an.

    @param stdscr: curses Screen

    @return: Weiterleitung zum Listenmenü
    """
    return auto_liste_menu(stdscr, filter_type="frei", title="Freie Autos")

def vergebene_autos(stdscr):
    """
    Zeigt alle aktuell vermieteten Autos an.

    @param stdscr: curses Screen

    @return: Weiterleitung zum Listenmenü
    """
    return auto_liste_menu(stdscr, filter_type="verliehen", title="Vermietete Autos")


# Menü welches je nach ausgewähltem Filter alle Autos, freie Autos oder vermietete Autos anzeigt
def auto_liste_menu(stdscr, filter_type, title):
    """
    Erstellt ein Menü zur Anzeige von Autos basierend auf einem Filter.

    @param stdscr: curses Screen
    @param filter_type: Filter ("alle", "frei", "verliehen")
    @param title: Titel des Menüs

    @return: Tupel aus Menüoptionen, Action-Map und Titel
    """
    curses.curs_set(0)

    menu_options = ["(0) ZURÜCK"]

    action_map = {
        0: lambda stdscr: main_menu()
    }

    garage = Garage()
    autos = garage.alle_autos()

    i = 1
    for kennzeichen, daten in autos.items():
        if filter_type == "frei" and daten["verliehen"]:
            continue
        if filter_type == "verliehen" and not daten["verliehen"]:
            continue

        menu_options.append(
            f"({i}) {kennzeichen} | {daten['marke']} | {daten['tagespreis']}€/Tag"
        )

        action_map[i] = lambda stdscr, k=kennzeichen: auto_options_menu(stdscr, k)

        i += 1

    return menu_options, action_map, title

# Menü zeigt die möglichen Aktionen an die für das Auto durchgeführt werden können
def auto_options_menu(stdscr, kennzeichen):
    """
    Zeigt Aktionen für ein ausgewähltes Auto an.

    @param stdscr: curses Screen
    @param kennzeichen: Kennzeichen des Autos

    @return: Tupel aus Menüoptionen, Action-Map und Titel
    """
    stdscr.refresh()
    curses.curs_set(0)

    garage = Garage()
    auto = garage.auto_finden(kennzeichen)

    menu_options = ["(0) ZURÜCK"]
    action_map = {
        0: lambda stdscr: autos_anzeigen(stdscr)
    }

    i = 1

    menu_options.append("(1) Auto löschen")
    action_map[i] = lambda stdscr: delete_and_refresh(stdscr, garage, kennzeichen)
    i += 1

    menu_options.append("(2) Auto bearbeiten")
    action_map[i] = lambda stdscr: auto_detail_menu(stdscr, kennzeichen)
    i += 1

    # nur wenn vermietet
    if auto["verliehen"]:
        menu_options.append(f"({i}) Freigeben")
        action_map[i] = lambda stdscr: freigeben_screen(stdscr, kennzeichen)
        i += 1

    # nur wenn frei
    if not auto["verliehen"]:
        menu_options.append(f"({i}) Vermieten")
        action_map[i] = lambda stdscr: vermieten_flow(stdscr, garage, kennzeichen)
        i += 1

    return menu_options, action_map, f"Auto {kennzeichen}"

# Funktion um ein Auto zu löschen und danach die Auto Liste zu aktualisieren
def delete_and_refresh(stdscr, garage: Garage, kennzeichen):
    """
    Löscht ein Auto und aktualisiert die Anzeige.

    @param stdscr: curses Screen
    @param garage: Garage-Instanz
    @param kennzeichen: Kennzeichen des Autos

    @return: Aktualisierte Autoliste
    """
    garage.auto_entfernen(kennzeichen)
    stdscr.refresh()
    stdscr.clear()
    # Nach dem Hinzufügen zum Menü zurückkehren
    return autos_anzeigen(stdscr)

# MENÜ, welches die Details eines Autos anzeigt, die mit deren Auswahl bearbeitet werden können
def auto_detail_menu(stdscr, kennzeichen):
    """
    Zeigt Details eines Autos und ermöglicht Bearbeitung einzelner Attribute.

    @param stdscr: curses Screen
    @param kennzeichen: Kennzeichen des Autos

    @return: Tupel aus Menüoptionen, Action-Map und Titel
    """
    curses.curs_set(0)
    auto = Garage().auto_finden(kennzeichen)

    menu_options = [
        "(0) BACK",
        "(1) # Kennzeichen: \t\t" + kennzeichen,
        "(2) # Marke: \t\t\t" + auto["marke"],
        "(3) # Modell: \t\t" + auto["modell"],
        "(4) # Baujahr: \t\t" + str(auto["baujahr"]),
        "(5) # Verbrauch in Litern: \t" + f"{auto['verbrauch']:.2f}",
        "(6) # Tagespreis in EUR: \t" + f"{auto['tagespreis']:.2f}",
    ]

    action_map = {
        0: lambda stdscr: auto_options_menu(stdscr, kennzeichen),
        1: lambda stdscr: auto_bearbeiten(stdscr, "kennzeichen", kennzeichen, auto),
        2: lambda stdscr: auto_bearbeiten(stdscr, "marke", kennzeichen, auto),
        3: lambda stdscr: auto_bearbeiten(stdscr, "modell", kennzeichen, auto),
        4: lambda stdscr: auto_bearbeiten(stdscr, "baujahr", kennzeichen, auto),
        5: lambda stdscr: auto_bearbeiten(stdscr, "verbrauch", kennzeichen, auto),
        6: lambda stdscr: auto_bearbeiten(stdscr, "tagespreis", kennzeichen, auto)
    }

    return menu_options, action_map, f"Auto {kennzeichen}"

# Funktion berechnet den erwarteten Umsatz nach aktuellem Stand der vermieteten Autos und zeigt diesen an
def umsatz(stdscr):
    """
    Berechnet und zeigt den erwarteten Gesamtumsatz aller Vermietungen.

    @param stdscr: curses Screen

    @return: Rückkehr zum Hauptmenü
    """
    garage = Garage()
    curses.curs_set(1) # setzt curser auf sichtbar
    stdscr.clear()
    stdscr.addstr(0, 0, f"Erwarteter Umsatz nach allen Rückgaben: {garage.umsatz_berechnen()}€.")
    stdscr.refresh()
    stdscr.getch()
    return main_menu()