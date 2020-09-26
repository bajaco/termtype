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
