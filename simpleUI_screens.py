from controller import Controller
import curses
from abc import ABC, abstractmethod

class Screen(ABC):
    def __init__(self, stdscr, ctrl):
        self._stdscr = stdscr
        self._ctrl = ctrl
        self.playlist_window_height = 0
        self.playlist_window_start = 0

        self.line_num = 0
        self.playlist_list_start = 0
        self.selection_symbol = '$'
        self.lines = []

    @abstractmethod
    def generate_lines(self):
        pass

    @abstractmethod
    def render_screen(self):
        pass

    @abstractmethod
    def execute_action(self):
        pass

    @abstractmethod
    def controls(self, k):
        pass

    def render_line(self, line):
        self._stdscr.addstr(line.offset, line.x_start, line.text)

    def add_playlists_list(self):
        names = self._ctrl.list_playlists_names()
        for i in range(min(len(names), self.playlist_window_height)):
            self.lines.append(Line(f"[ {'x' if self._ctrl.selected[i + self.playlist_list_start] else ' '}"
                                   f" ] {names[i + self.playlist_list_start]}"[:Line.width - 1],
                                   self.playlist_window_start + i, 3, self._ctrl.select_playlist))

        if len(names) > self.playlist_window_height + self.playlist_list_start + 1:
            self.lines.append(Line("      ..."[:Line.width - 1], Line.height - 5, 3, interactive=False))

    def render_common_elements(self):
        # Render status bar
        statusbarstr = "Press 'q' to exit | left/right - navigate | up/down - show more playlists"
        self._stdscr.attron(curses.color_pair(3))
        self._stdscr.addstr(Line.height - 1, 0, statusbarstr)
        self._stdscr.addstr(Line.height - 1, len(statusbarstr), " " * (Line.width - len(statusbarstr) - 1))
        self._stdscr.attroff(curses.color_pair(3))

        # Print selection symbol
        self._stdscr.addstr(self.lines[self.line_num].offset,
                            self.lines[self.line_num].x_start - 2,
                            self.selection_symbol)


class MainScreen(Screen):
    instance = None

    def __init__(self, stdscr, ctrl):
        super().__init__(stdscr, ctrl)
        self.playlist_window_height = Line.height - 17
        self.playlist_window_start = 12

    def generate_lines(self):
        self.lines = [
            Line(f"{self._ctrl.username}   |"[:Line.width - 1], 1, Line.x_center() - 15, line_break=False),
            Line("log out"[:Line.width - 1], 1, Line.x_center() + 3, lambda num: self.print_line_num(num)),
            Line(f"{self._ctrl.current_track_title()}"[:Line.width - 1], 6, interactive=False),
            Line("|<<"[:Line.width - 1], 8, Line.x_center() - 9, self._ctrl.prev_track, line_break=False),
            Line("(_▶_)"[:Line.width - 1], 8, Line.x_center() - 3, self._ctrl.play_current_track, line_break=False),  # pause
            Line(">>|"[:Line.width - 1], 8, Line.x_center() + 5, self._ctrl.next_track, line_break=False),
            Line("<3"[:Line.width - 1], 8, Line.x_center() + 13),
            Line((" -" * (Line.x_center()))[:Line.width - 1], 10, interactive=False),
        ]

        self.add_playlists_list()
        self.lines.append(Line("Change playlist list"[:Line.width - 1], Line.height - 3, 3,
                               self.switch_to_playlist_choice_screen))

    def render_screen(self):
        self.generate_lines()

        self._stdscr.addstr(1, self.lines[0].x_start, self.lines[0].text)  # curses.color_pair(1)

        # Turning on attributes for title
        # stdscr.attron(curses.color_pair(2))
        self._stdscr.attron(curses.A_BOLD)

        # Rendering title
        self.render_line(self.lines[0])
        self.render_line(self.lines[1])

        # Turning off attributes for title
        # stdscr.attroff(curses.color_pair(2))
        self._stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        for i in range(2, len(self.lines)):
            self.render_line(self.lines[i])

        self.render_common_elements()

    def execute_action(self):
        if self.lines[self.line_num].function is None:
            return

        if self.line_num == 1:
            (self.lines[self.line_num]).function(self.line_num)
        elif self.line_num == len(self.lines) - 1:
            (self.lines[self.line_num]).function()
        else:
            self._ctrl.name = (self.lines[self.line_num]).text[6::]
            if (self.lines[self.line_num]).function is not None:
                (self.lines[self.line_num]).function()

    def controls(self, k):
        # if k != -1:
        #     print(f'controls: {k}')
        if k == ord(' '):
            self.execute_action()
        elif k == curses.KEY_RIGHT:
            found = False
            old_line_num = self.line_num
            while self.line_num < len(self.lines) - 1:
                self.line_num = min(self.line_num + 1, len(self.lines) - 1)
                if (self.lines[self.line_num]).interactive:
                    found = True
                    break
            if not found: self.line_num = old_line_num
        elif k == curses.KEY_LEFT:
            found = False
            old_line_num = self.line_num
            while self.line_num > 0:
                self.line_num = max(self.line_num - 1, 0)
                if (self.lines[self.line_num]).interactive:
                    found = True
                    break
            if not found: self.line_num = old_line_num
        if k == curses.KEY_DOWN:
            self.playlist_list_start = min(self.playlist_list_start + 1,
                                           len(self._ctrl.playlists) - self.playlist_window_height - 1)
        elif k == curses.KEY_UP:
            self.playlist_list_start = max(self.playlist_list_start - 1, 0)

    def print_line_num(self, line_num):
        print(line_num)

    def switch_to_playlist_choice_screen(self):
        self._ctrl.screen = PlaylistChoiceScreen.get_instance()

    @staticmethod
    def get_instance(stdscr = None, ctrl = None):
        if MainScreen.instance is None:
            MainScreen.instance = MainScreen(stdscr, ctrl)

        return MainScreen.instance


class PlaylistChoiceScreen(Screen):
    instance = None

    def __init__(self, stdscr, ctrl):
        super().__init__(stdscr, ctrl)
        self.playlist_window_height = Line.height - 10
        self.playlist_window_start = 5

    def generate_lines(self):
        self.lines = [
            Line("Choose the playlists you want to add songs to"[:Line.width - 1], 1, -1, interactive=False),
            Line(f"Go back"[:Line.width - 1], 3, 9, self.switch_to_main_screen),
        ]

        self.add_playlists_list()

    def render_screen(self):
        self.generate_lines()

        for i in range(len(self.lines)):
            self.render_line(self.lines[i])

        self.render_common_elements()

    def execute_action(self):
        if (self.lines[self.line_num]).function is not None:
            (self.lines[self.line_num]).function()

    def controls(self, k):
        if k == ord(' '):
            self.execute_action()
        elif k == curses.KEY_RIGHT:
            found = False
            old_line_num = self.line_num
            while self.line_num < len(self.lines) - 1:
                self.line_num = min(self.line_num + 1, len(self.lines) - 1)
                if self.lines[self.line_num].interactive:
                    found = True
                    break
            if not found: self.line_num = old_line_num
        elif k == curses.KEY_LEFT:
            found = False
            old_line_num = self.line_num
            while self.line_num > 0:
                self.line_num = max(self.line_num - 1, 0)
                if (self.lines[self.line_num]).interactive:
                    found = True
                    break
            if not found: self.line_num = old_line_num
        if k == curses.KEY_DOWN:
            self.playlist_list_start = min(self.playlist_list_start + 1,
                                           len(self._ctrl.playlists) - self.playlist_window_height - 1)
        elif k == curses.KEY_UP:
            self.playlist_list_start = max(self.playlist_list_start - 1, 0)

    def switch_to_main_screen(self):
        self._ctrl.screen = MainScreen.get_instance()
        print(self._ctrl.screen)

    @staticmethod
    def get_instance(stdscr = None, ctrl = None):
        if PlaylistChoiceScreen.instance is None:
            PlaylistChoiceScreen.instance = PlaylistChoiceScreen(stdscr, ctrl)

        return PlaylistChoiceScreen.instance


class LoadingScreen(Screen):
    instance = None

    def __init__(self, stdscr, ctrl):
        super().__init__(stdscr, ctrl)

    def generate_lines(self):
        pass

    def render_screen(self):
        loading_string = "Loading ..."
        x_start = int(Line.width // 2) - int(len(loading_string) // 2)
        self._stdscr.addstr(Line.y_center(), x_start, loading_string)

    def execute_action(self):
        pass

    def controls(self, k):
        pass

    @staticmethod
    def get_instance(stdscr=None, ctrl=None):
        if LoadingScreen.instance is None:
            LoadingScreen.instance = LoadingScreen(stdscr, ctrl)

        return LoadingScreen.instance


class Line:
    width = 0
    height = 0

    def __init__(self, text: str, offset, x_start=-1, function=None, interactive=True, line_break=True):
        self.text = text
        self.offset = offset
        self.x_start = self.calculate_start(text) if x_start == -1 else x_start
        self.interactive = interactive
        self.line_break = line_break
        self.function = function

    @staticmethod
    def x_center():
        return int(Line.width // 2)

    @staticmethod
    def y_center():
        return int(Line.height // 2)

    @staticmethod
    def calculate_start(text: str):
        return int((Line.width // 2) - (len(text) // 2) - len(text) % 2)
