import curses
from enum import Enum
from bs4 import BeautifulSoup
import urllib.request
from classes import Keyboard
from classes import Menu
from classes import Buffer



def main(stdscr):
    menu = Menu(stdscr,'Intro', 'Help', 'Play', 'Stats', 'Exit')
    keyboard = Keyboard(stdscr)
    mode = 1
    key = 0
    curses.curs_set(0)
    while mode != 5:
        
        if mode == 1:
            stdscr.clear()
            menu.print_splash()
            menu.print_menu()
            stdscr.refresh()
            menu.navigate(stdscr.getkey())

    stringBuffer = Buffer()
'''
    key = 0
    while key != 'q':
        key = stdscr.getkey()
        stringBuffer.insert(key)
        stdscr.addstr(0, 0, stringBuffer.get_text())
        stdscr.refresh()
'''     

curses.wrapper(main)

