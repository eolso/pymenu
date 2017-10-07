#!/usr/bin/env python3.5
"""MODULE DESCRIPTION
"""
import curses
import curses.panel

class Menu(object):
    """Object to hold everything related to a menu itself. This includes window
    to window interaction, as well as accepting and parsing input"""
    def __init__(self):
        self.windows = []
        self.selection = 0

        self.screen = curses.initscr()
        curses.noecho()
        curses.start_color()
        curses.cbreak()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        curses.endwin()

    def add_window(self, name, rows, cols):
        """Adds a window to the menu, returns said window"""
        new_window = WinManager(name, rows, cols)
        self.windows.append(new_window)
        return new_window

    def get_wm(self, window_title):
        """Returns the WindowManager that contains the window window_title
        Throws a NameError if the window_title cannot be found
        """
        for window in self.windows:
            if window_title == window.win_name:
                return window
        raise NameError('Window ' + window_title + ' does not exist')

    def show_window(self, window_title):
        """Shows a specified window"""
        self.selection = 0
        window_mgr = self.get_wm(window_title)
        self.get_input(window_mgr)

    def increment_selection(self, window_mgr):
        """Safely increments the selection tracker"""
        if self.selection < len(window_mgr.entries) - 1:
            self.selection += 1

    def decrement_selection(self):
        """Safely decrements the selection counter"""
        if self.selection > 0:
            self.selection -= 1

    def run_instruction(self, window_entry):
        """Parses a stored instruction and attempts to run it"""
        instruction_set = window_entry['instruction'].split(':')
        if instruction_set[0] == 'show':
            self.show_window(instruction_set[1].strip())
        # elif instruction_set[0] == 'hide':
        #     self.hide_window(instruction_set[1].strip())
        elif instruction_set[0] == 'py':
            exec(instruction_set[1].strip())

    def get_input(self, window_mgr):
        """Gets keyboard input from the user until an specified interrupt key
        is encountered"""
        while True:
            window_mgr.print_menu(self.selection)
            key_press = window_mgr.window.getch()

            if key_press == curses.KEY_UP:
                self.decrement_selection()
            elif key_press == curses.KEY_DOWN:
                self.increment_selection(window_mgr)
            elif key_press == curses.KEY_ENTER or key_press == 10 or key_press == 13:
                self.run_instruction(window_mgr.entries[self.selection])
            elif key_press == ord('q'):
                break


class WinManager(object):
    """Object to hold everything related to a curses window. All functions
    that act soley on a generated window should be contained here"""
    def __init__(self, name, screeny, screenx):
        self.win_name = name
        self.pady = 5
        self.padx = 5
        self.window = curses.newwin(screeny, screenx)
        self.entries = []
        self.panel = curses.panel.new_panel(self.window)

        self.window.keypad(1)

    def set_padding(self, row_pad, col_pad):
        """Sets the padding for menu entries. Units are in rows/columns"""
        self.pady = row_pad
        self.padx = col_pad

    def add_entry(self, entry_string, instruction):
        """Adds a text entry to the window. Separates multiple entries by a
        single row"""
        entry = {'text': entry_string, 'instruction': instruction}
        self.entries.append(entry)

    def print_menu(self, selection):
        """Prints out the stored entries to the window and then shows it"""
        self.window.erase()
        self.window.addstr(0, 0, self.win_name)

        for index, entry in enumerate(self.entries):
            if index == selection:
                self.window.addstr(self.pady + index, self.padx, entry['text'],
                                   curses.A_STANDOUT)
            else:
                self.window.addstr(self.pady + index, self.padx, entry['text'])

        self.window.refresh()
        self.panel.show()
