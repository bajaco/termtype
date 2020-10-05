from enum import Enum
import json
import curses
import wikipedia
import string
import time

class Timer:
    def __init__(self):
        self.beginning = None
        self.end = None
        self.timing = False
        self.duration = None

    def start(self):
        self.beginning = time.time()
        self.timing = True

    def stop(self):
        self.end = time.time()
        self.timing = False
        self.duration = self.end - self.beginning

    def is_timing(self):
        return self.timing

    def get_duration(self):
        return self.duration

    def get_pretty_duration(self):
        dur = self.duration
        durstring = ''
        if dur > 3600:
            hours = int(dur/3600)
            durstring += str(hours)
            dursting += ' hours '
            dur -= 3600 * hours
            
        if dur > 60:
            minutes = int(dur/60)
            durstring += str(minutes)
            durstring += ' minutes '
            dur -= 60 * minutes
            
        durstring += str(int(dur))
        durstring += ' seconds'
        return durstring
            

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
    
    def has(self, c):
        return c.lower() in self.KEYS

    def transform_text(self, text):
        newtext = []
        for c in text:
            if c.lower() in self.KEYS:
                newtext.append(self.KEYS[c.lower()])
            else:
                newtext.append(c)
        return ''.join(newtext)

    def error_text(self, master, typed):
        new_text = [] 
        for i,c in enumerate(typed):
            if c == master[i]:
                if c == ' ':
                    new_text.append(' ')
                else:
                    new_text.append('_')
            else:
                new_text.append('X')
            
        return ''.join(new_text)



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
    
    def __delete(self):
        if self.length > self.position:
            self.text = self.text[:self.position] + self.text[self.position + 1:]
            self.length -= 1

    def insert(self, insert_string):
        self.text = (self.text[0:self.position] + insert_string + self.text[self.position:self.length])
        self.length += len(insert_string)
        self.position += len(insert_string)

    def get_text(self):
        return self.text

    def input(self, c, keyboard):
        if keyboard.has(chr(c)):
            self.insert(chr(c))
        else:
            if c == curses.KEY_BACKSPACE:
                self.__left()
                self.__delete()

    def clear(self):
        self.text = ''
        self.length = 0
        self.position = 0

    def new_errors(self,comparison_text):
        errors = 0
        for i,c in enumerate(self.text):
            if i < len(comparison_text):
                if c != comparison_text[i]:
                    errors += 1
        return errors


    def get_count(self):
        return len(self.text.split())

#formatter class for putting text in window
class Formatter:

    def __init__(self, stdscr, text, line_height=1, 
            vertical_offset=0, vertical_buffer=0):
        self.master_text = text
        self.text = self.master_text
        self.words = text.split()
        self.lines = []
        self.pages = []
        self.line_height = line_height
        self.vertical_offset = vertical_offset
        self.vertical_buffer = vertical_buffer
        self.stdscr = stdscr
    
    def set_master(self,text):
        self.master_text = text

    def reset(self):
        self.text = self.master_text
        self.words = self.text.split()
        self.lines = []
        self.pages = []

    def remove_words(self, index):
        new_text = []
        words = self.text.split()
        removed_words = words[:index]
        words = words[index:]
        self.master_text = ' '.join(words)
        return ' '.join(removed_words)
    
    def out_of_words(self):
        if len(self.pages) > 0:
            return False
        return True


    def make_line(self):
        line = []
        line_length = 0
        for word in self.words:
            line_length += len(word) + 1
            if line_length < (self.stdscr.getmaxyx()[1] / 2):
                line.append(word)
            else:
                break
        self.lines.append(line)
        self.words = self.words[len(line):]
    
    def make_all_lines(self):
        while len(self.words) > 0:
            self.make_line()

    def make_page(self):
        index = int(self.stdscr.getmaxyx()[0] / self.line_height 
                - self.vertical_buffer)
        self.pages.append(self.lines[0:index])
        self.lines = self.lines[index:]

    def make_all_pages(self):
        while len(self.lines) > 0:
            self.make_page()

    def dump_text(self):
        text = []
        for page in self.pages:
            for line in page:
                for word in line:
                    text.append(word)
        return ' '.join(text)
    
    #convert text into pages of lines that fit the terminal window
    #and then display the first page. The first page will be destroyed 
    #when conifrmed as a matching entry
    def print_text(self):
        self.reset()
        self.words = self.text.split()
        self.make_all_lines()
        self.make_all_pages()
        if len(self.pages) > 0:
            page = self.pages[0]
            for i, line in enumerate(page):
                text = ' '.join(line)
                text = list(text)
                text = ' '.join(text)
                self.stdscr.addstr(self.vertical_offset + 
                        (self.line_height * i),0,text)


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
        
        if key == curses.KEY_UP and self.active_item > 1:
            self.active_item -= 1
        elif key == curses.KEY_DOWN and self.active_item < self.menu_length:
            self.active_item += 1
        elif key == curses.KEY_ENTER or key == 10:
            return self.active_item
        return 0

class Wiki:
    
    def __init__(self):
        self.page = None
        while self.page is None:
            try:
                title = wikipedia.random()
                self.page = wikipedia.page(title=title)
            except:
                pass


    def get_page(self):
        printable = set(string.printable)
        content = self.page.content
        
        #remove characters that cannot be displayed
        content = ''.join(filter(lambda x: x in printable, content))
        
        #remove references and other errata
        #content = content.split('==')
        #content = content[0]

        return content

