import curses

from functions import draw_menu
from auto import Auto
from garage import Garage

def main():
    # auto = Auto("ROW-RS-100", "BMW", "E46", "2002", "205000", "8,5", "50")
    # garage = Garage()
    # garage.auto_hinzufügen(auto)
    print("Hello World!")
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()