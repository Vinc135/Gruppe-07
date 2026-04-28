import curses

from functions import draw_menu

def main():
    print("Hello World!")
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()