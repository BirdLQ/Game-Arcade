import curses
import time
import random
from methods.ascii_dict import *
import main_menu
import gameoflife


snowflake = ['*', '+', '.']

def get_screen(stdscr):
    h, w = stdscr.getmaxyx()
    return (h, w)

def max_dimensions(window):
    height, width = window.getmaxyx()
    return height - 2, width - 1

def draw_moon(stdscr):
    curses.mousemask(1)
    moon_pos = []
    moon = [
        '  **   ',
        '   *** ',
        '    ***',
        '    ***',
        '   *** ',
        '  **   ',
    ]
    start_position = max_dimensions(stdscr)[1] - 10
    stdscr.attrset(curses.color_pair(1))
    for height, line in enumerate(moon, start=1):
        for position, sym in enumerate(line, start=start_position):
            stdscr.addch(height, position, sym)
            moon_pos.append([height, position])
    stdscr.attrset(curses.color_pair(0))
    key = stdscr.getch()
    if key == curses.KEY_MOUSE:
        _, x, y, _, _ = curses.getmouse()
        if [y, x] in moon_pos:
            gameoflife.gol_start()

def build_cabin(stdscr):
    h, w = get_screen(stdscr)
    snowDict = {}
    if h > 7 and w > 16:
        for pos in smallHouse.keys():
            if pos[0] == 0:
                new_pos = (h-7,int(2*w/3+pos[1]))
            if pos[0] == 1:
                new_pos = (h-6,int(2*w/3+pos[1]))
            if pos[0] == 2:
                new_pos = (h-5,int(2*w/3+pos[1]))
            if pos[0] == 3:
                new_pos = (h-4,int(2*w/3+pos[1]))
            if pos[0] == 4:
                new_pos = (h-3,int(2*w/3+pos[1]))
            if pos[0] == 5:
                new_pos = (h-2,int(2*w/3+pos[1]))
            snowDict[new_pos] = smallHouse[pos]
    return snowDict

# create a snowflake! we need to know its starting position (in the x)
# which can be any value between 1 and max width, need to choose the char
def create_flake(stdscr):
    w = get_screen(stdscr)[1]
    x = random.randrange(1, w)
    flake = random.choice(snowflake)
    return (x, flake)

def new_snow(stdscr, snowDict):
    w = get_screen(stdscr)[1]
    x, flake = create_flake(stdscr)
    # dont forget curses goes like "y,x" for some dumbass reason
    snow = {(0,x): flake}
    return snow

def draw_snow(stdscr, snowDict):
    h = get_screen(stdscr)[0]
    for key in snowDict.keys():
        if key[0] < h-1:
            stdscr.addch(key[0], key[1], snowDict[key])
        else:
            pass
"""
def pack_snow(stdscr, snowDict):
    i, j = 0, 0
    w, h = get_screen(stdscrn)
    for j in range (1,w):
        if snowDict[((h-3),j)] in snowflake:
            for i in range(0,3):
                snowDict[h-]
"""

def move_snow(stdscr, snowDict):
    movedSnowDict = {}
    h = get_screen(stdscr)[0]
    for pos in snowDict.keys():
        if pos[0] < h-2 and (pos[0]+1,pos[1]) not in snowDict.keys():
            new_pos = (pos[0]+1, pos[1])
        else:
            new_pos = pos
        movedSnowDict[new_pos] = snowDict[pos]
    return movedSnowDict

def main(stdscr):
    snowDict = build_cabin(stdscr)
    curses.curs_set(0)
    stdscr.nodelay(1)
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    msg = 'COMING SOON !'
    y, x = get_screen(stdscr)[0]//2, get_screen(stdscr)[1]//2-len(msg)//2
    while True:
        key = stdscr.getch()
        if key == curses.KEY_EXIT or key == 27:
            break
        stdscr.clear()
        draw_moon(stdscr)
        snowDict.update(new_snow(stdscr, snowDict))
        draw_snow(stdscr, snowDict)
        snowDict = move_snow(stdscr, snowDict)
        stdscr.addstr(y, x, msg, curses.A_STANDOUT)
        stdscr.refresh()
        time.sleep(.1)
    stdscr.nodelay(0)
    main_menu.run_app()
    
def Snow():
    curses.wrapper(main)