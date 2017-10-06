#!/usr/bin/env python3.5

import curses
import curses.panel

class Menu(object):
    """CLASS DESCRIPTION"""
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
        new_window = WinManager(name, rows, cols)
        self.windows.append(new_window)
        return new_window

    def get_wm(self, window_title):
        for window in self.windows:
            if window_title == window.win_name:
                return window
        raise NameError('Window ' + window_title + ' does not exist')

    def show_window(self, window_title):
        self.selection = 0
        window_mgr = self.get_wm(window_title)
        self.get_input(window_mgr)

    def increment_selection(self, window_mgr):
        if self.selection < len(window_mgr.entries) - 1:
            self.selection += 1

    def decrement_selection(self):
        if self.selection > 0:
            self.selection -= 1

    def run_instruction(self, window_entry):
        instruction_set = window_entry['instruction'].split(':')
        if instruction_set[0] == 'show':
            self.show_window(instruction_set[1].strip())
        elif instruction_set[0] == 'hide':
            self.hide_window(instruction_set[1].strip())
        elif instruction_set[0] == 'py':
            exec(instruction_set[1].strip())

    def get_input(self, window_mgr):
        while True:
            window_mgr.print_menu(self.selection)
            c = window_mgr.window.getch()

            if c == curses.KEY_UP:
                self.decrement_selection()
            elif c == curses.KEY_DOWN:
                self.increment_selection(window_mgr)
            elif c == curses.KEY_ENTER or c == 10 or c == 13:
                self.run_instruction(window_mgr.entries[self.selection])
            elif c == ord('q'):
                break


class WinManager(object):
    def __init__(self, name, screeny, screenx):
        self.win_name = name
        self.pady = 5
        self.padx = 5
        self.window = curses.newwin(screeny, screenx)
        self.entries = []
        self.panel = curses.panel.new_panel(self.window)

        self.window.keypad(1)

    def set_padding(self, row_pad, col_pad):
        self.pady = row_pad
        self.padx = col_pad

    def add_entry(self, entry_string, instruction):
        entry = {'text': entry_string, 'instruction': instruction}
        self.entries.append(entry)

    def print_menu(self, selection):
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
