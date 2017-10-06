#!/usr/bin/env python3.5
"""This program does stuff
"""

import ecc
import menu
from subprocess import call

def main():
    with menu.MenuHandler() as mh:
        mh.add_window('utilities', 30, 30)
        mh.add_window('options', 30, 30)

        mh.add_entry('root', '1. Utilities', 'show: utilities')
        mh.add_entry('root', '2. Options', 'show: options')
        mh.add_entry('root', '3. Exit', 'py: exit()')

        mh.add_entry('utilities', '1. Do cool function', '')
        mh.add_entry('utilities', '2. Do other cool function', '')
        mh.add_entry('utilities', '3. Go back', 'show: root')

        mh.add_entry('options', '1. Configure some option', '')
        mh.add_entry('options', '2. Go back', 'show: root')

        mh.show_window('root')

if __name__ == '__main__':
    main()
