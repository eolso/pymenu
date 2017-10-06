#!/usr/bin/env python3.5

import curses
import curses.panel
from sys import exit

class MenuHandler(object):
    """CLASS DESCRIPTION"""
    windows = []
    selection = 0
    start_row = 5
    start_col = 5

    def __init__(self):
        new_window = curses.initscr()
        new_window.keypad(1)
        new_window_panel = curses.panel.new_panel(new_window)
        new_window_panel.hide()
        new_menu_entries = []
        window_info = {'title': 'root', 'window': new_window,
                       'panel': new_window_panel, 'entries': new_menu_entries}
        self.windows.append(window_info)
        curses.noecho()
        curses.start_color()
        curses.cbreak()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        curses.endwin()

    # keep here
    def add_window(self, name, rows, cols):
        new_window = curses.newwin(rows, cols)
        new_window.keypad(1)
        new_window_panel = curses.panel.new_panel(new_window)
        new_window_panel.hide()
        new_menu_entries = []
        window_info = {'title': name, 'window': new_window,
                       'panel': new_window_panel, 'entries': new_menu_entries}
        self.windows.append(window_info)

    #  move to window class
    def set_padding(self, row_pad, col_pad):
        self.start_row = row_pad
        self.start_col = col_pad

    # keep here?
    def get_windata(self, window_title):
        for window in self.windows:
            if window_title == window['title']:
                return window
        raise NameError('Window ' + window_title + ' does not exist')

    # not sure
    def get_size(self, window_title='root'):
        root = self.get_windata(window_title)
        return root['window'].getmaxyx()

    # keep here
    def show_window(self, window_title):
        self.selection = 0
        windata = self.get_windata(window_title)
        windata['panel'].show()
        windata['window'].refresh()
        self.print_menu(windata)
        self.get_input(windata)

    # keep here
    def hide_window(self, window_title):
        windata = self.get_windata(window_title)
        windata['panel'].hide()
        windata['window'].refresh()

    # move to window class
    def add_entry(self, window_title, entry_string, instruction):
        windata = self.get_windata(window_title)
        entry = MenuItem()
        entry.configure(entry_string, instruction)
        windata['entries'].append(entry)

    # move to window class
    def print_menu(self, windata):
        windata['window'].erase()
        for index, entry in enumerate(windata['entries']):
            if index == self.selection:
                windata['window'].addstr(self.start_row + index, self.start_col,
                                         entry.text, curses.A_STANDOUT)
            else:
                windata['window'].addstr(self.start_row + index, self.start_col, entry.text)
        windata['window'].refresh()

    # keep here
    def increment_selection(self, windata):
        if self.selection < len(windata['entries']) - 1:
            self.selection += 1

    # keep here
    def decrement_selection(self):
        if self.selection > 0:
            self.selection -= 1

    # keep here
    def run_instruction(self, menu_item):
        instruction_set = menu_item.instruction.split(':')
        if instruction_set[0] == 'show':
            self.show_window(instruction_set[1].strip())
        elif instruction_set[0] == 'hide':
            self.hide_window(instruction_set[1].strip())
        elif instruction_set[0] == 'py':
            exec(instruction_set[1].strip())

    # keep here
    def get_input(self, windata):
        while True:
            c = windata['window'].getch()

            if c == curses.KEY_UP:
                self.decrement_selection()
            elif c == curses.KEY_DOWN:
                self.increment_selection(windata)
            elif c == curses.KEY_ENTER or c == 10 or c == 13:
                self.run_instruction(windata['entries'][self.selection])
            elif c == ord('q'):
                break

            self.print_menu(windata)

class MenuItem(object):
    text = None
    instruction = None

    def __init__(self):
        self.text = "Generic menu item"
        self.instruction = ""

    def configure(self, new_text, new_instruction):
        self.text = new_text
        self.instruction = new_instruction
