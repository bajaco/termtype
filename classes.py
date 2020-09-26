from enum import Enum
import json
import curses

class Keyboard:
    def __init__(self,stdscr):
        self.KEYS = None
        try:
            with open('keys.json', 'r') as f:
                self.KEYS = json.load(f)
        except OSError:
            print('Could not load keys.json!')

    def get_finger(self, key):
        return self.KEYS[key]


#string buffer class for editing strings
class Buffer:
    def __init__(self,initial_text = ''):
        self.text = initial_text
        self.length = len(self.text)
        self.position = len(self.text)

    def __left(self):
        if self.position > 0:
            self.position -= 1
    
    def __right(self):
        if self.position < self.length:
            self.position += 1

    def insert(self, insert_string):
        self.text = (self.text[0:self.position] + insert_text +  
                self.text[self.position:self.length])
        self.length += len(insert_string)
        self.position += len(insert_string)

    def get_text(self):
        return self.text

#formatter class for putting text in window
class Formatter:

    def __init__(self, stdscr, text):
        self.text = text.rstrip()
        self.words = text.split(' ')
        self.lines = []
        self.pages = []
        self.stdscr = stdscr
        
    def get_line(self):
        line = []
        line_length = 0
        for word in self.words:
            line_length += len(word) + 1
            if line_length < self.stdscr.getmaxyx()[1] / 2:
                line.append(word)
        self.lines.append(line)
        self.words = self.words[len(line):]

    def get_all_lines(self):
        while len(self.words) > 0:
            self.get_line()

    def get_page(self):
        index = int(self.stdscr.getmaxyx()[0])
        self.pages.append(self.lines[0:index])
        self.lines = self.lines[index:]

    def get_all_pages(self):
        while len(self.lines) > 0:
            self.get_page()

    def print_text(self):
        self.get_all_lines()
        self.get_all_pages()
        page = self.pages[0]
        for i, line in enumerate(page):
            text = ' '.join(line)
            text = list(text)
            text = ' '.join(text)
            self.stdscr.addstr(i,0,text)

    def debug(self):
        debug_string = ''
        for page in self.pages:
            debug_string += 'PAGE: '
            for line in page:
                debug_string += 'LINE: '
                for word in line:
                    dubug_string += word
        self.stdscr.addstr(0, 0, debug_string)

            


class Menu:
    def __init__(self, stdscr, *args):
        self.menu_items = args
        self.menu_length = len(self.menu_items)
        self.stdscr = stdscr
        self.active_item = 1
    
    def print_splash(self):
        splash = '''
       Welcome to . . .
  |                           |                       
  __|   _ \   __|  __ `__ \   __|  |   |  __ \    _ \ 
  |     __/  |     |   |   |  |    |   |  |   |   __/ 
 \__| \___| _|    _|  _|  _| \__| \__, |  .__/  \___| 
                                  ____/  _|           
            ''' 
        self.stdscr.addstr(splash)

    def print_menu(self):
        for i,v in enumerate(self.menu_items):
            if i + 1 == self.active_item:
                self.stdscr.addstr(i + 8, 0, 
                        str(i + 1) + '. ' + v, curses.A_STANDOUT)
            else:
                self.stdscr.addstr(i + 8, 0, str(i + 1) + '. ' + v)

    def navigate(self,key):
        self.stdscr.addstr(str(self.active_item))
        if key == curses.KEY_UP and self.active_item > 1:
            self.active_item -= 1
        elif key == curses.KEY_DOWN and self.active_item < self.menu_length:
            self.active_item += 1
        elif key == curses.KEY_ENTER or key == 10:
            return self.active_item
        return 1
