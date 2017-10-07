#!/usr/bin/env python3.5
import pymenu

def main():
    with pymenu.Menu() as menu:
        # Get screen size for new windows
        screen_size = menu.screen.getmaxyx()

        # Create two new windows
        main_window = menu.add_window('Main Window', screen_size[0], screen_size[1])
        sub_window = menu.add_window('Sub Window', screen_size[0], screen_size[1])

        # Add menu entries to main window
        main_window.add_entry('Go to Sub Window', 'show: Sub Window')
        main_window.add_entry('Don\'t do anything', '')
        main_window.add_entry('Exit', 'py: exit()')

        # Add menu entries to sub window
        sub_window.add_entry('Don\'t go back', '')
        sub_window.add_entry('Go back', 'show: Main Window')

        # Start program on main window
        menu.show_window('Main Window')

if __name__ == '__main__':
    main()
