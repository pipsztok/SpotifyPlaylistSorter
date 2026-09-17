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


def add_lines(ctrl) -> list[Line]:
    lines_list = [
        Line(f"{ctrl.username}   |"[:Line.width-1], 1, Line.x_center() - 15, line_break=False),
        Line("log out"[:Line.width - 1], 1, Line.x_center() + 3),
        Line(f"{ctrl.recent_track_title()}"[:Line.width - 1], 6),
        Line("|<<"[:Line.width - 1], 8, Line.x_center() - 9, line_break=False),
        Line("(_▶_)"[:Line.width - 1], 8, Line.x_center() - 3, line_break=False),
        Line(">>|"[:Line.width - 1], 8, Line.x_center() + 5, line_break=False),
        Line("<3"[:Line.width - 1], 8, Line.x_center() + 13),
        # Line("          (_▶_)   >>|     <3"[:Line.width - 1]),
        Line((" -"*(Line.x_center()))[:Line.width - 1], 10, interactive=False),
        # Line("[ x ] Playlist name 1"[:Line.width - 1], 12, 3),
        # Line("[   ] Playlist name 2"[:Line.width - 1], 13, 3),
        # Line("[   ] Playlist name 3"[:Line.width - 1], 14, 3),
        # Line("Change playlist list"[:Line.width - 1], 16, 3),
        # Line(""[:Line.width - 1], 17),
    ]

    names = ctrl.list_playlists_names()
    for i in range(min(len(names), Line.playlist_window_height)):
        lines_list.append(Line(f"[   ] {names[i + ctrl.playlist_list_start]}"[:Line.width - 1], 12 + i, 3))

    if len(names) > Line.playlist_window_height + ctrl.playlist_list_start + 1:
        lines_list.append(Line("      ..."[:Line.width - 1], Line.height - 5, 3, interactive=False))
    lines_list.append(Line("Change playlist list"[:Line.width - 1], Line.height - 3, 3))

    return lines_list

def render_line(stdscr, line):
    stdscr.addstr(line.offset, line.x_start, line.text)

def render_main_menu(stdscr, ctrl, k):
    cursor_x = 0
    cursor_y = 0
    selection_symbol = '$'

    cursor_x = max(0, cursor_x)
    cursor_x = min(Line.width - 1, cursor_x)

    cursor_y = max(0, cursor_y)
    cursor_y = min(Line.height - 1, cursor_y)

    lines = add_lines(ctrl)

    if k == curses.KEY_RIGHT:
        while ctrl.line_num < len(lines) - 1:
            ctrl.line_num = min(ctrl.line_num + 1, len(lines) - 1)
            if lines[ctrl.line_num].interactive:
                break
    elif k == curses.KEY_LEFT:
        while ctrl.line_num > 0:
            ctrl.line_num = max(ctrl.line_num - 1, 0)
            if lines[ctrl.line_num].interactive:
                break
    elif k == curses.KEY_DOWN:
        ctrl.playlist_list_start = min(ctrl.playlist_list_start + 1, len(ctrl.playlists)-Line.playlist_window_height-1)
    elif k == curses.KEY_UP:
        ctrl.playlist_list_start = max(ctrl.playlist_list_start - 1, 0)

    # Declaration of strings
    # keystr = "Last key pressed: {}".format(k)[:width-1]
    statusbarstr = "Press 'q' to exit | left/right - navigate | up/down - show more playlists"
    if k == 0:
        pass
        # keystr = "No key press detected..."[:width-1]

    # Centering calculations
    start_y = int((Line.height // 2) - 8)

    # Rendering some text
    whstr = "Width: {}, Height: {}".format(Line.width, Line.height)
    # print(lines[0].x_start, lines[0].text)
    stdscr.addstr(1, lines[0].x_start, lines[0].text)  # curses.color_pair(1)

    # Render status bar
    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(Line.height - 1, 0, statusbarstr)
    stdscr.addstr(Line.height - 1, len(statusbarstr), " " * (Line.width - len(statusbarstr) - 1))
    stdscr.attroff(curses.color_pair(3))

    # Turning on attributes for title
    # stdscr.attron(curses.color_pair(2))
    stdscr.attron(curses.A_BOLD)

    # Rendering title
    # stdscr.addstr(start_y - 1, lines[1].x_start, lines[1].text)
    render_line(stdscr, lines[0])
    render_line(stdscr, lines[1])

    # Turning off attributes for title
    # stdscr.attroff(curses.color_pair(2))
    stdscr.attroff(curses.A_BOLD)

    # Print rest of text
    for i in range(2, len(lines)):
        render_line(stdscr, lines[i])

    # Print selection symbol
    stdscr.addstr(lines[ctrl.line_num].offset, lines[ctrl.line_num].x_start - 2, selection_symbol)
    # stdscr.addstr(start_y + 1, lines[2].x_start, lines[2].text)
    # stdscr.addstr(start_y + 3, lines[3].x_start, lines[3].text)

    # stdscr.addstr(start_y + 10, 0, lines[4].text)
    # stdscr.addstr(start_y + 12, 0, lines[5].text)
    # stdscr.addstr(start_y + 14, 0, lines[6].text)
    # stdscr.addstr(start_y + 16, 0, lines[7].text)
    stdscr.move(cursor_y, cursor_x)

def render_loading_screen(stdscr):
    height, width = stdscr.getmaxyx()
    loading_string = "Loading ..."
    x_start = int(width // 2) - int(len(loading_string) // 2)
    y_center = int(height // 2)
    # print()
    stdscr.addstr(y_center, x_start, loading_string)

def draw_menu(stdscr):
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

        # if k == curses.KEY_DOWN:
        #     cursor_y = cursor_y + 1
        # elif k == curses.KEY_UP:
        #     cursor_y = cursor_y - 1

        if not ctrl.data_loaded:
            render_loading_screen(stdscr)
        else:
            render_main_menu(stdscr, ctrl, k)
        # render_main_menu(stdscr, ctrl, k)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()

