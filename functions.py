import curses
from action_type_attribute import *
from garage import Garage 

def draw_menu(stdscr):

    curses.curs_set(0)  # Hide the cursor

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
    prompt="Use arrow keys to navigate and press Right Arrow to select: ",
):
    while True:
        stdscr.clear()
        if title:
            stdscr.addstr(0, 0, title)
            title_offset = 1
        else:
            title_offset = 0

        # Menu starts from line 1 (or 0 if no title)
        for idx, row in enumerate(menu_options):
            if idx == current_row:
                stdscr.addstr(idx + title_offset + 1, 0, f"> {row}", curses.A_REVERSE)
            else:
                stdscr.addstr(idx + title_offset + 1, 0, f"  {row}")

        stdscr.addstr(len(menu_options) + title_offset + 2, 0, prompt)

        key = stdscr.getch()  # Get user input

        if key == curses.KEY_UP:  # If the UP arrow key is pressed
            current_row = (current_row - 1) % len(menu_options)  # Wrap around using modulo
        elif key == curses.KEY_DOWN:  # If the DOWN arrow key is pressed
            current_row = (current_row + 1) % len(menu_options)  # Wrap around using modulo
        elif key == curses.KEY_RIGHT:  # If the RIGHT arrow key is pressed
            if current_row in action_map:

                entry = action_map[current_row]

                if entry[1] == ActionType.ACTION:
                    entry[0](stdscr)
                    continue
                elif entry[1] == ActionType.ACTION_RETURN:
                    entry[0](stdscr)
                    return menu_options, action_map, title
                else:
                    a, b, c = entry[0](stdscr)
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
                stdscr.addstr(len(menu_options) + title_offset + 3, 0, "Invalid input, please try again.")
                stdscr.refresh()
                curses.napms(1000)  # Wait 1 second before redrawing the menu

        stdscr.refresh()

## Menu #####################################################################
def main_menu():
    menu_options = [
        "(0) Auto hinzufügen",
        "(1) Alle Autos anzeigen",
        "(2) Freie Autos anzeigen",
        "(3) Vermietete Autos anzeigen"
    ]

    action_map = {
        0: (lambda stdscr: auto_hinzufuegen(stdscr), ActionType.MENU), #LENNOX
        1: (lambda stdscr: autos_anzeigen(stdscr), ActionType.MENU),
        2: (lambda stdscr: freie_autos(stdscr), ActionType.MENU),
        3: (lambda stdscr: vergebene_autos(stdscr), ActionType.MENU),
    }

    return menu_options, action_map, "Main Menu"

############ Filter Typen

def autos_anzeigen(stdscr):
    return auto_liste_menu(stdscr, filter_type="alle", title="Alle Autos")

def freie_autos(stdscr):
    return auto_liste_menu(stdscr, filter_type="frei", title="Freie Autos")

def vergebene_autos(stdscr):
    return auto_liste_menu(stdscr, filter_type="verliehen", title="Vermietete Autos")


#### Allgemeines Listen Menü für alle Autos
def auto_liste_menu(stdscr, filter_type, title):
    curses.curs_set(0)

    menu_options = ["(0) BACK"]

    action_map = {
        0: (lambda stdscr: main_menu(), ActionType.MENU)
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

        action_map[i] = (
            lambda stdscr, k=kennzeichen: auto_detail_menu(stdscr, k),
            ActionType.MENU
        )

        i += 1

    return menu_options, action_map, title

def auto_detail_menu(stdscr, kennzeichen):
    curses.curs_set(0)

    garage = Garage()
    auto = garage.auto_finden(kennzeichen)

    menu_options = ["(0) BACK"]
    action_map = {
        0: (lambda stdscr: autos_anzeigen(stdscr), ActionType.MENU)
    }

    i = 1

    menu_options.append("(1) Auto löschen")
    action_map[i] = (lambda stdscr: delete_and_refresh(stdscr, garage, kennzeichen), ActionType.ACTION)
    i += 1

    menu_options.append("(2) Auto bearbeiten")
    action_map[i] = (lambda stdscr: auto_bearbeiten(stdscr, kennzeichen), ActionType.MENU)
    i += 1

    # nur wenn vermietet
    if auto["verliehen"]:
        menu_options.append(f"({i}) Freigeben")
        action_map[i] = (
            lambda stdscr: garage.zurueckgeben(kennzeichen),
            ActionType.ACTION
        )
        i += 1

    # nur wenn frei
    if not auto["verliehen"]:
        menu_options.append(f"({i}) Vermieten")
        action_map[i] = (
            lambda stdscr: vermieten_flow(stdscr, garage, kennzeichen),
            ActionType.ACTION
        )
        i += 1

    return menu_options, action_map, f"Auto {kennzeichen}"

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

def delete_and_refresh(stdscr, garage, kennzeichen):
    garage.auto_entfernen(kennzeichen)
    autos_anzeigen(stdscr)
