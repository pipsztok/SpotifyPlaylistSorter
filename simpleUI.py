import sys,os
import curses
from spotify_helper import SpotifyHelper


class Controller:
    def __init__(self):
        self.sh = SpotifyHelper()
        self.username = self.sh.get_username()
        self.recent = self.sh.get_recently_played_tracks()
        self.playlists = self.sh.get_user_playlist()
        self.playlists_to_add = []
        self.playlists_to_remove = []
        self.playlists_tracks = {}

    def recent_track_title(self):
        return self.recent[0]['track']['name']

    def list_tracks_in_playlists(self):
        # for each playlist do 'playlist_id' -> ['song1_id', 'song2_id', ...]
        pass

    # find which playlists is the song in


class Line:
    width = 0

    def __init__(self, text: str, offset, x_start=-1, line_break=True):
        self.text = text
        self.offset = offset
        self.x_start = self.calculate_start(text) if x_start == -1 else x_start
        self.line_break = line_break

    @staticmethod
    def calculate_start(text: str):
        return int((Line.width // 2) - (len(text) // 2) - len(text) % 2)


def add_lines(ctrl) -> list[Line]:
    x_center = int(Line.width // 2)
    lines_list = [
        Line("Username   |"[:Line.width-1], 1, x_center - 12, line_break=False),
        Line("log out"[:Line.width - 1], 1, x_center + 3),
        Line(f"{ctrl.recent_track_title()}"[:Line.width - 1], 6),
        Line("|<<"[:Line.width - 1], 8, x_center - 9, line_break=False),
        Line("(_▶_)"[:Line.width - 1], 8, x_center - 3, line_break=False),
        Line(">>|"[:Line.width - 1], 8, x_center + 5, line_break=False),
        Line("<3"[:Line.width - 1], 8, x_center + 13),
        # Line("          (_▶_)   >>|     <3"[:Line.width - 1]),
        Line("- - - - - - - - - - - - - - - - - - - - - - - - - -"[:Line.width - 1], 10),
        Line("[ x ] Playlist name 1"[:Line.width - 1], 12, 3),
        Line("[   ] Playlist name 2"[:Line.width - 1], 13, 3),
        Line("[   ] Playlist name 3"[:Line.width - 1], 14, 3),
        Line("Change playlist list"[:Line.width - 1], 16, 3),
        Line(""[:Line.width - 1], 17),
    ]
    return lines_list

def render_line(stdscr, line):
    stdscr.addstr(line.offset, line.x_start, line.text)

def draw_menu(stdscr):
    k = 0
    cursor_x = 0
    cursor_y = 0
    selection_symbol = '$'
    line_num = 0
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
        height, width = stdscr.getmaxyx()
        Line.width = width

        # if k == curses.KEY_DOWN:
        #     cursor_y = cursor_y + 1
        # elif k == curses.KEY_UP:
        #     cursor_y = cursor_y - 1


        cursor_x = max(0, cursor_x)
        cursor_x = min(width-1, cursor_x)

        cursor_y = max(0, cursor_y)
        cursor_y = min(height-1, cursor_y)

        lines = add_lines(ctrl)

        if k == curses.KEY_RIGHT:
            # cursor_x = cursor_x + 1
            line_num = min(line_num + 1, len(lines)-1)
        elif k == curses.KEY_LEFT:
            # cursor_x = cursor_x - 1
            line_num = max(line_num - 1, 0)

        # Declaration of strings
        # keystr = "Last key pressed: {}".format(k)[:width-1]
        statusbarstr = "Press 'q' to exit | STATUS BAR | Pos: {}, {}".format(cursor_x, cursor_y)
        if k == 0:
            pass
            # keystr = "No key press detected..."[:width-1]

        # Centering calculations
        start_y = int((height // 2) - 8)

        # Rendering some text
        whstr = "Width: {}, Height: {}".format(width, height)
        # print(lines[0].x_start, lines[0].text)
        stdscr.addstr(1, lines[0].x_start, lines[0].text)  # curses.color_pair(1)

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
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
        for i in range (2, len(lines)-1):
            render_line(stdscr, lines[i])

        stdscr.addstr(lines[line_num].offset, lines[line_num].x_start-2, selection_symbol)
        # stdscr.addstr(start_y + 1, lines[2].x_start, lines[2].text)
        # stdscr.addstr(start_y + 3, lines[3].x_start, lines[3].text)

        # stdscr.addstr(start_y + 10, 0, lines[4].text)
        # stdscr.addstr(start_y + 12, 0, lines[5].text)
        # stdscr.addstr(start_y + 14, 0, lines[6].text)
        # stdscr.addstr(start_y + 16, 0, lines[7].text)
        stdscr.move(cursor_y, cursor_x)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()

