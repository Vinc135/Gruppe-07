import curses
from action_type_attribute import *

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
        "(0) Garagen Menü",
        "(1) Autos ausleihen",
    ]

    action_map = {
        0: (lambda stdscr: garage_menu(stdscr), ActionType.MENU),
        1: (lambda stdscr: autos_ausleihen(stdscr), ActionType.MENU),
    }

    return menu_options, action_map, "Main menu"

def garage_menu(stdscr):
    curses.curs_set(0)  # Hide the cursor
    menu_options = [
        "(0) BACK",
        "(1) Schleife mit Autos"
    ]
    
    action_map = {
        0: (lambda stdscr: main_menu(), ActionType.MENU),  # Back to main menu
        1: (
            lambda stdscr: #funktion von Auto,
            ActionType.ACTION,
        )
    }

    return menu_options, action_map, "Garagen Menü"

def autos_ausleihen(stdscr):
    curses.curs_set(0)  # Hide the cursor
    menu_options = [
        "(0) BACK",
        "(1) BMW...",
        "(2) VW...",
        "(3) Skoda..."
    ]
    
    action_map = {
        0: (lambda stdscr: main_menu(), ActionType.MENU),  # Back to main menu
        1: (
            lambda stdscr: perform_action_with_output(stdscr, mcl.output_one_draftshield_status()),
            ActionType.ACTION,
        )
    }

    return menu_options, action_map, "Autos ausleihen Menü"