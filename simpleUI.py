import sys,os
import curses
from controller import Controller
from simpleUI_screens import MainScreen, PlaylistChoiceScreen, LoadingScreen, Line


def draw_screen(stdscr):
    stdscr.nodelay(True)
    k = 0
    height, width = stdscr.getmaxyx()
    Line.width = width
    Line.height = height

    ctrl = Controller()
    PlaylistChoiceScreen.get_instance(stdscr, ctrl)
    ctrl.screen = LoadingScreen.get_instance(stdscr, ctrl)

    ctrl.load_spotify_data(MainScreen.get_instance(stdscr, ctrl))

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Loop where k is the last character pressed
    while k != ord('q'):

        # Initialization
        stdscr.clear()

        # Render screen
        # print(ctrl.screen)
        ctrl.screen.render_screen()

        # Pass control to the screen
        ctrl.screen.controls(k)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

def main():
    curses.wrapper(draw_screen)

if __name__ == "__main__":
    main()

