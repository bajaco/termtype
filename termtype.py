import curses
from enum import Enum
from bs4 import BeautifulSoup
import urllib.request

KEYS = {
        '~': '1',
        '`': '1',
        '!': '1',
        '1': '1',
        'q': '1',
        'a': '1',
        'z': '1',
        '@': '2',
        '2': '2',
        'w': '2',
        's': '2',
        'x': '2',
        '#': '3',
        '3': '3',
        'e': '3',
        'd': '3',
        'c': '3',
        '$': '4',
        '4': '4',
        '%': '4',
        '5': '4',
        'r': '4',
        't': '4',
        'f': '4',
        'g': '4',
        'v': '4',
        'b': '4',
        '^': '5',
        '6': '5',
        '&': '5',
        '7': '5',
        'y': '5',
        'u': '5',
        'h': '5',
        'j': '5',
        'n': '5',
        'm': '5',
        '*': '6',
        '8': '6',
        'i': '6',
        'k': '6',
        '<' : '6',
        ',' : '6',
        '(': '7',
        '9': '7',
        'o': '7',
        'l': '7',
        '>': '7',
        '.': '7',
        ')': '8',
        '0': '8',
        '_': '8',
        '-': '8',
        '+': '8',
        '=': '8',
        'p': '8',
        '{': '8',
        '[': '8',
        '}': '8',
        ']': '8',
        '|': '8',
        '\\': '8',
        ':': '8',
        ';': '8',
        '"': '8',
        "'": '8',
        '?': '8',
        '/': '8'
}


class Mode(Enum):
    INTRO = 0
    HELP = 1
    GAME = 2
    RESULT = 3
    STATS = 4
    EXIT = 5

class Menu:
    def __init__(self, stdscr, *args):
        self.menu_items = args
        self.screen = stdscr
        self.active = 0
        self.min = 0
        self.max = len(self.menu_items) - 1
    
    def print_menu(self):
        ypos = 0
        for index, item in enumerate(self.menu_items):
            if index == self.active:
                self.screen.addstr(ypos + 2, self.screen.getmaxyx()[1] - len(item) -2, item, curses.A_REVERSE)
            else:
                self.screen.addstr(ypos + 2, self.screen.getmaxyx()[1] - len(item) - 2, item)
            ypos += 1

    def nav(self, key):
        if key == curses.KEY_UP:
            if self.active > self.min:
                self.active -= 1
        elif key == curses.KEY_DOWN:
            if self.active < self.max:
                self.active += 1
        elif key == curses.KEY_ENTER or key == 10:
            return True , self.menu_items[self.active]
        return False, self.menu_items[self.active]

def key_to_finger(line):
    finger_line = ''
    for char in line:
        c = char.lower()
        if c == ' ':
            finger_line += c
        elif c in KEYS:
            finger_line += KEYS[c]
        else:
            finger_line += '*'
    return finger_line

def strip_spaces(s):
    return [c for c in s if c != ' ']

def space_string(s):
    news = ''
    for c in s:
        news += c + ' '
    return news

def print_string(y, x, screen, s):
    sar = s.split()
    line = ''
    lines = []
    maxwidth = screen.getmaxyx()[1] - 3
    for word in sar:
        if len(line) + len(word) + 1 < maxwidth:
            line += word + ' '
        else:
            lines.append(line)
            line = word + ' '
    lines.append(line)
    lineno = 0
    for line in lines:
        screen.addstr(y + lineno, x + 2, line)
        lineno += 1

def get_lines(screen, s, div):
    sar = s.split()
    line = ''
    lines = []
    maxwidth = round(screen.getmaxyx()[1] / div)
    for word in sar:
        if len(line) + len(word) + 1 < maxwidth:
            line += word + ' '
        else:
            lines.append(line)
            line = word + ' '
    lines.append(line)
    return lines

try:
    stdscr = curses.initscr()
    curses.cbreak()
    curses.noecho()
    curses.curs_set(0)
    stdscr.keypad(True)
    
    mode = Mode.INTRO
    count = 0
    menu = Menu(stdscr,'Help','Play','Stats','Credits','Quit')
    while True:
        if mode == Mode.INTRO:
            stdscr.erase()
            greeting = '''
       Welcome to . . .
  |                           |                       
  __|   _ \   __|  __ `__ \   __|  |   |  __ \    _ \ 
  |     __/  |     |   |   |  |    |   |  |   |   __/ 
 \__| \___| _|    _|  _|  _| \__| \__, |  .__/  \___| 
                                  ____/  _|           
            '''
            stdscr.addstr(greeting)
            stdscr.border(0)
            menu.print_menu()
            instructions = '''
Termtype is a terminal-based tool for developing touch-typing skills. Select play to load a random wikipedia article, and type it out, line by line. Termtype will indicate which finger is supposed to be used to press a key, 1-4 for the left hand and 5-8 for the right. Lines are only accepted when typed correctly.
'''
            print_string(8,0,stdscr,instructions)
            key = 0
            keys = [curses.KEY_DOWN, curses.KEY_UP, curses.KEY_ENTER, 10]
            while key not in keys:
                key = stdscr.getch()
                if key in keys:
                   response = menu.nav(key)
                   if response[0]:
                       if response[1] == 'Quit':
                           mode = Mode.EXIT
                       elif response[1] == 'Play':
                           mode = Mode.GAME
        elif mode == Mode.GAME:
            curses.curs_set(1)
            stdscr.erase()
            stdscr.border(0)
            menu.print_menu()
            html = urllib.request.urlopen(
                    'https://en.wikipedia.org/wiki/Special:Random').read()
            soup = BeautifulSoup(html,'html.parser')
            ps = [p.text for p in soup.find_all('p')]
            
            for paragraph in ps:
                stdscr.erase()
                stdscr.border(0)
                length = len(paragraph)
                lines = get_lines(stdscr,paragraph,2)
                lines = [line for line in lines if len(line) > 0]
                for i, line in enumerate(lines):
                    spaced_line = space_string(line)
                    stdscr.addstr(i*6 + 2,2,spaced_line)
                    stdscr.addstr(i*6 + 4,2,key_to_finger(spaced_line))
                    stdscr.move(i*6 + 6, 2)
                    stdscr.refresh()
                    line_incorrect = True
                    entered_line = ''
                    curpos=0
                    while(line_incorrect):
                        c = stdscr.getkey()
                        if c == ' ':
                            stdscr.addstr(' ')
                            stdscr.move(stdscr.getyx()[0],stdscr.getyx()[1] + 1)
                            entered_line = entered_line[0:curpos] + ' ' + entered_line[curpos + 1: len(entered_line)]
                            curpos += 1
                        elif c.lower() in KEYS:
                            stdscr.addstr(c)
                            stdscr.move(stdscr.getyx()[0],stdscr.getyx()[1] + 1)
                            entered_line += c
                            curpos += 1
                        elif  c  == 'KEY_BACKSPACE':
                            stdscr.move(stdscr.getyx()[0],stdscr.getyx()[1] - 2)
                            entered_line = entered_line[0:curpos - 1] + entered_line[curpos:len(entered_line)]
                            curpos -= 1
                        elif c == 'KEY_LEFT':
                            stdscr.move(stdscr.getyx()[0],stdscr.getyx()[1] - 2)
                            curpos -= 1
                        elif c == 'KEY_RIGHT':
                            stdscr.move(stdscr.getyx()[0],stdscr.getyx()[1] + 2)
                            curpos += 1
                        elif c == '\n':
                            if strip_spaces(line) == strip_spaces(entered_line):
                                line_incorrect = False
        elif mode == Mode.EXIT:
            break

finally:
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
