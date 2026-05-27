import curses
from action_type_attribute import *
from garage import Garage 
from auto import Auto
import datetime

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
            lambda stdscr: freigeben_screen(stdscr, kennzeichen),
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


def list_auto_details_menu(stdscr, kennzeichen):
    curses.curs_set(0)
    auto = Garage().auto_finden(kennzeichen)

    menu_options = [
        "(0) BACK",
        "(1) # Kennzeichen: \t\t" + kennzeichen,
        "(2) # Marke: \t\t\t" + auto["marke"],
        "(3) # Modell: \t\t" + auto["modell"],
        "(4) # Baujahr: \t\t" + str(auto["baujahr"]),
        "(5) # Verbrauch in Litern: \t" + str(auto["verbrauch"]),
        "(6) # Tagespreis in EUR: \t" + str(auto["tagespreis"]),
    ]

    action_map = {
        0: (lambda stdscr: auto_detail_menu(stdscr, kennzeichen), ActionType.MENU),
        1: (lambda stdscr: auto_bearbeiten(stdscr, "kennzeichen", kennzeichen, auto), ActionType.MENU),
        2: (lambda stdscr: auto_bearbeiten(stdscr, "marke", kennzeichen, auto), ActionType.MENU),
        3: (lambda stdscr: auto_bearbeiten(stdscr, "modell", kennzeichen, auto), ActionType.MENU),
        4: (lambda stdscr: auto_bearbeiten(stdscr, "baujahr", kennzeichen, auto), ActionType.MENU),
        5: (lambda stdscr: auto_bearbeiten(stdscr, "verbrauch", kennzeichen, auto), ActionType.MENU),
        6: (lambda stdscr: auto_bearbeiten(stdscr, "tagespreis", kennzeichen, auto), ActionType.MENU)
    }

    return menu_options, action_map, f"Auto {kennzeichen}"

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
        return list_auto_details_menu(stdscr, kennzeichen)

    stdscr.clear()
    stdscr.addstr(0, 0, f"Bitte wählen Sie einen neuen Wert für {filter}:")
    stdscr.addstr(2, 0, f"Aktueller Wert: {aktueller_wert}")
    stdscr.addstr(4, 0, "Neuer Wert: ")
    curses.curs_set(1)
    curses.echo()
    neuer_wert = stdscr.getstr(4, 12, 20).decode("utf-8").strip()
    curses.curs_set(0)
    curses.noecho()

    if neuer_wert == "":
        stdscr.addstr(6, 0, "Fehler: Es wurde kein neuer Wert eingegeben.")
        stdscr.refresh()
        curses.napms(2000)
        return list_auto_details_menu(stdscr, kennzeichen)

    isValid = True
    if filter == "kennzeichen":
        
        neuer_wert = neuer_wert.strip().upper()

        # altes auto löschen, neues mit aktualisiertem kennzeichen hinzufügen
        ####################

    elif filter == "marke":
        
        if neuer_wert is None or auto is None or neuer_wert.strip() == "":
            isValid = False        
        auto["marke"] = neuer_wert

    elif filter == "modell":
        
        if neuer_wert is None or auto is None or neuer_wert.strip() == "":
            isValid = False        
        auto["modell"] = neuer_wert

    elif filter == "baujahr":

        neuer_wert = int(neuer_wert)
        if neuer_wert is None or auto is None or neuer_wert > datetime.date.today().year or neuer_wert < 1500:
            isValid = False        
        auto["baujahr"] = neuer_wert 

    elif filter == "verbrauch":

        neuer_wert = float(neuer_wert.replace(",", "."))
        if neuer_wert is None or auto is None or neuer_wert < 0:
            isValid = False        
        auto["verbrauch"] = neuer_wert 

    elif filter == "tagespreis":
        
        neuer_wert = float(neuer_wert.replace(",", "."))
        if neuer_wert is None or auto is None or neuer_wert < 0:
            isValid = False        
        auto["tagespreis"] = neuer_wert

    
    if isValid == False:
        stdscr.addstr(6, 0, "Fehler: Es wurde kein gültiger Wert eingegeben.")
        stdscr.refresh()
        curses.napms(2000)
        return list_auto_details_menu(stdscr, kennzeichen)

    ###############################################################
    # JSON updaten
    garage = Garage()
    garage.auto_update(kennzeichen, auto)

    if filter == "kennzeichen":
        return list_auto_details_menu(stdscr, neuer_wert)

    return list_auto_details_menu(stdscr, kennzeichen)


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

    return main_menu()