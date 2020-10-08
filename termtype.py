import curses
from enum import Enum
from bs4 import BeautifulSoup
import urllib.request
from classes import Keyboard
from classes import Menu
from classes import Buffer
from classes import Formatter
from classes import Wiki
from classes import Timer
from classes import Database


def main(stdscr):
    menu = Menu(stdscr, 'Help', 'Play', 'Stats', 'Exit')
    keyboard = Keyboard(stdscr)
    database = Database(stdscr)
    mode = 0
    key = 0
    curses.curs_set(0)
    curses.noecho()
    curses.use_default_colors()
    
    #selct mode based on menu options
    while mode != 4: 
        if mode == 0:
            stdscr.clear()
            menu.print_splash()
            menu.print_menu()
            mode = menu.navigate(stdscr.getch())
            stdscr.refresh()
        elif mode == 1:
            mode = 4 
        elif mode == 2:
            
            #initialization for play mode
            wiki = Wiki()
            typing_buffer = Buffer()
            page_text = wiki.get_page()
            guide_text = keyboard.transform_text(page_text)
            error_text = ''
            errors = 0
            entered_words = 0
            timer = Timer()
            
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

            #gameplay loop
            while(True):
                #clear string and print from formatters
                stdscr.clear()
                wiki_formatter.print_text() 
                guide_formatter.print_text()
                typing_formatter.print_text()
                error_formatter.print_text()
                
                #break if there are no more words to be typed and show statistics
                if wiki_formatter.out_of_words():
                    timer.stop()
                    break
                
                #if key is enter, remove page from wiki and guide formatters
                stdscr.refresh()
                c = stdscr.getch()

                #if key is ENTER
                if c == 10: 
                    count = typing_buffer.get_count()
                    entered_words += count
                    removed = wiki_formatter.remove_words(count)
                    guide_formatter.remove_words(count)
                    errors += typing_buffer.new_errors(removed)
                    typing_buffer.clear()
                    error_formatter.set_master('')
                    typing_formatter.set_master('')
                
                #if key is ESC
                elif c == 27:
                    count = typing_buffer.get_count()
                    entered_words += count
                    if entered_words == 0:
                        break
                    timer.stop()
                    removed = wiki_formatter.remove_words(count)
                    guide_formatter.remove_words(count)
                    errors += typing_buffer.new_errors(removed)
                    break
                
                #other keys
                else:
                    #start timing if necessary
                    if not timer.is_timing():
                        timer.start()

                    typing_buffer.input(c, keyboard)
                    typing_formatter.set_master(typing_buffer.get_text())
                    error_formatter.set_master(keyboard.error_text(
                        wiki_formatter.dump_text(), typing_buffer.get_text()))

            #statistics loop
            while(True):
                if entered_words == 0:
                    mode = 0
                    break
                stdscr.clear()
                database.write(timer.get_duration(), entered_words, errors)
                database.read() 
                database.print_stats()
                stdscr.refresh()


                c = stdscr.getkey()
                if c == 'q':
                    mode = 4
                    break
                else:
                    mode = 0
                    break

        elif mode == 3:
            
            while(True):
                stdscr.clear()
                database.read() 
                database.print_stats()
                stdscr.refresh()
                c = stdscr.getkey()
                if c == 'q':
                    mode = 4
                    break
                else:
                    mode = 0
                    break

curses.wrapper(main)
