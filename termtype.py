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
    
    #selct mode based on menu options
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
            typing_buffer = Buffer()
            page_text = wiki.get_page()
            guide_text = keyboard.transform_text(page_text)
            error_text = ''
            
            #Formatter for article
            wiki_formatter = Formatter(stdscr, page_text,
                    line_height=6, vertical_offset=1, vertical_buffer=0)
            
            #Formatter for finger indication
            guide_formatter = Formatter(stdscr, guide_text,
                    line_height=6, vertical_offset=0, vertical_buffer=0)
           
            #Formatter for typed text
            typing_formatter = Formatter(stdscr, typing_buffer.get_text(),
                    line_height=6, vertical_offset=2, vertical_buffer=0)

            #Formatter for error text
            error_formatter = Formatter(stdscr, error_text,
                    line_height=6, vertical_offset=3, vertical_buffer=0)

            


            while(True):
                #clear string and print from formatters
                stdscr.clear()
                wiki_formatter.print_text() 
                guide_formatter.print_text()
                typing_formatter.print_text()
                error_formatter.print_text()
                
                #if key is enter, remove page from wiki and guide formatters
                stdscr.refresh()
                c = stdscr.getch()
                if c == 10: 
                    count = typing_buffer.get_count()
                    wiki_formatter.remove_words(count)
                    guide_formatter.remove_words(count)
                    typing_buffer.clear()
                    error_formatter.set_master('')
                    typing_formatter.set_master('')
                else:
                    typing_buffer.input(c, keyboard)
                    typing_formatter.set_master(typing_buffer.get_text())
                    error_formatter.set_master(keyboard.error_text(
                        wiki_formatter.dump_text(), typing_buffer.get_text()))

        elif mode == 4:
            mode = 5

curses.wrapper(main)
