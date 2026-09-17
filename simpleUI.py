import sys,os
import curses
from controller import Controller


class Line:
    width = 0
    height = 0
    playlist_window_height = 0

    def __init__(self, text: str, offset, x_start=-1, interactive=True, line_break=True):
        self.text = text
        self.offset = offset
        self.x_start = self.calculate_start(text) if x_start == -1 else x_start
        self.interactive = interactive
        self.line_break = line_break

    @staticmethod
    def x_center():
        return int(Line.width // 2)

    @staticmethod
    def y_center():
        return int(Line.height // 2)

    @staticmethod
    def calculate_start(text: str):
        return int((Line.width // 2) - (len(text) // 2) - len(text) % 2)


def generate_lines_main_screen(ctrl):
    ctrl.lines = [
        Line(f"{ctrl.username}   |"[:Line.width-1], 1, Line.x_center() - 15, line_break=False),
        Line("log out"[:Line.width - 1], 1, Line.x_center() + 3),
        Line(f"{ctrl.recent_track_title()}"[:Line.width - 1], 6),
        Line("|<<"[:Line.width - 1], 8, Line.x_center() - 9, line_break=False),
        Line("(_▶_)"[:Line.width - 1], 8, Line.x_center() - 3, line_break=False),
        Line(">>|"[:Line.width - 1], 8, Line.x_center() + 5, line_break=False),
        Line("<3"[:Line.width - 1], 8, Line.x_center() + 13),
        Line((" -"*(Line.x_center()))[:Line.width - 1], 10, interactive=False),
    ]

    add_playlists_list(ctrl)
    ctrl.lines.append(Line("Change playlist list"[:Line.width - 1], Line.height - 3, 3))

def generate_lines_playlist_choice_screen(ctrl):
    ctrl.lines = [
        Line("Choose the playlists you want to add songs to"[:Line.width - 1], 1, -1, interactive=False),
        Line(f"Go back"[:Line.width - 1], 3, 9),
    ]

    add_playlists_list(ctrl)

def add_playlists_list(ctrl):
    names = ctrl.list_playlists_names()
    for i in range(min(len(names), Line.playlist_window_height)):
        ctrl.lines.append(Line(f"[   ] {names[i + ctrl.playlist_list_start]}"[:Line.width - 1], 12 + i, 3))

    if len(names) > Line.playlist_window_height + ctrl.playlist_list_start + 1:
        ctrl.lines.append(Line("      ..."[:Line.width - 1], Line.height - 5, 3, interactive=False))

def render_line(stdscr, line):
    stdscr.addstr(line.offset, line.x_start, line.text)

def render_main_screen(stdscr, ctrl):
    generate_lines_main_screen(ctrl)

    stdscr.addstr(1, ctrl.lines[0].x_start, ctrl.lines[0].text)  # curses.color_pair(1)

    # Turning on attributes for title
    # stdscr.attron(curses.color_pair(2))
    stdscr.attron(curses.A_BOLD)

    # Rendering title
    render_line(stdscr, ctrl.lines[0])
    render_line(stdscr, ctrl.lines[1])

    # Turning off attributes for title
    # stdscr.attroff(curses.color_pair(2))
    stdscr.attroff(curses.A_BOLD)

    # Print rest of text
    for i in range(2, len(ctrl.lines)):
        render_line(stdscr, ctrl.lines[i])

def render_loading_screen(stdscr):
    loading_string = "Loading ..."
    x_start = int(Line.width // 2) - int(len(loading_string) // 2)
    # print()
    stdscr.addstr(Line.y_center(), x_start, loading_string)

def render_playlist_choice_screen(stdscr, ctrl):
    generate_lines_playlist_choice_screen(ctrl)

    for i in range(len(ctrl.lines)):
        render_line(stdscr, ctrl.lines[i])


def draw_screen(stdscr):
    stdscr.nodelay(True)
    k = 0
    height, width = stdscr.getmaxyx()
    Line.width = width
    Line.height = height
    Line.playlist_window_height = Line.height - 17
    ctrl = Controller()

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

        if not ctrl.data_loaded:
            render_loading_screen(stdscr)
            continue
        else:
            render_main_screen(stdscr, ctrl)
            # render_playlist_choice_screen(stdscr, ctrl)
        # render_main_menu(stdscr, ctrl, k)

        if k == curses.KEY_RIGHT:
            while ctrl.line_num < len(ctrl.lines) - 1:
                ctrl.line_num = min(ctrl.line_num + 1, len(ctrl.lines) - 1)
                if ctrl.lines[ctrl.line_num].interactive:
                    break
        elif k == curses.KEY_LEFT:
            while ctrl.line_num > 0:
                ctrl.line_num = max(ctrl.line_num - 1, 0)
                if ctrl.lines[ctrl.line_num].interactive:
                    break
        if k == curses.KEY_DOWN:
            ctrl.playlist_list_start = min(ctrl.playlist_list_start + 1,
                                           len(ctrl.playlists) - Line.playlist_window_height - 1)
        elif k == curses.KEY_UP:
            ctrl.playlist_list_start = max(ctrl.playlist_list_start - 1, 0)

        # Render status bar
        statusbarstr = "Press 'q' to exit | left/right - navigate | up/down - show more playlists"
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(Line.height - 1, 0, statusbarstr)
        stdscr.addstr(Line.height - 1, len(statusbarstr), " " * (Line.width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Print selection symbol
        stdscr.addstr(ctrl.lines[ctrl.line_num].offset, ctrl.lines[ctrl.line_num].x_start - 2, ctrl.selection_symbol)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

def main():
    curses.wrapper(draw_screen)

if __name__ == "__main__":
    main()

