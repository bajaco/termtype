import curses
from enum import Enum
from bs4 import BeautifulSoup
import urllib.request
from classes import Keyboard
from classes import Menu
from classes import Buffer
from classes import Formatter
from classes import Wiki


def main(stdscr):
    menu = Menu(stdscr,'Intro', 'Help', 'Play', 'Stats', 'Exit')
    keyboard = Keyboard(stdscr)
    mode = 1
    key = 0
    curses.curs_set(0)
    curses.noecho()
    while mode != 5: 
        if mode == 1:
            stdscr.clear()
            menu.print_splash()
            menu.print_menu()
            mode = menu.navigate(stdscr.getch())
            stdscr.refresh()
        elif mode == 2:
            mode = 5 
        elif mode == 3:
            wiki = Wiki()
            while(True):
                text = 'One two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'             
                stdscr.clear()
                
                formatter = Formatter(stdscr, wiki.get_page(),
                        line_height=3, vertical_offset=2)
                formatter.print_text()
                stdscr.refresh()
                key = stdscr.getch()

        elif mode == 4:
            mode = 5

curses.wrapper(main)
