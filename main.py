from functions import draw_menu
import curses

def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()