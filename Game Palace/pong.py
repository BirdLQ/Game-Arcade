import curses, random, time
from curses import textpad
from methods.menus import *

m_menu = ['1 player', '2 player', 'Return home']
botmenu = ['Easy', 'Medium', 'Hard']
s_menu = ['Play again', 'Save score', 'Return home']

def draw_board(stdscr, box):
    textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])
    
    for i in range(box[0][0]+1, box[1][0], 2):
            stdscr.addch(i, box[1][1]//2+1, '|')  
    
    stdscr.refresh()
    

def draw_paddle(stdscr, box, y, x):
    for i in range(6):
        stdscr.addch(y + i, x, ' ', curses.color_pair(2))
            
    stdscr.refresh()

def collision(stdscr, ball, walls, direction, player, comp):
    '''
    if ball[0] in (walls[1] or walls[3]):
        return -direction
    elif ball[1] in (walls[0] or walls[2]):
        return -direction
    '''
    print('ball', ball)
    print('player', player)
    for i in range(6):
        if ball[0] == player[0]+i and ball[1] == player[1]+1:
            return True
        elif ball[0] == comp[0]+i and ball[1] == comp[1]:
            return True
        
    
def draw_ball(stdscr, walls, ball, ball_speed, player, comp, direction):
    stdscr.addch(ball[0], ball[1], ' ', curses.color_pair(2))
    
    if collision(stdscr, ball, walls, direction, player, comp):
        direction = -direction
    
    ball[1] -= (1 * direction)
    
    stdscr.timeout(120)
    
def draw_score(stdscr):
    pass

def main(stdscr):
    curses.curs_set(0)  
    stdscr.nodelay(1)
    
    #set color pair
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_WHITE)
    
    #current row main menu
    current_row = 0
    #current row sub menu
    submenu_row = 0
    #current row exit menu
    exit_row = 1
    
    #box limits
    sh, sw = stdscr.getmaxyx()
    box = [[int(sh*0.10), int(sw*0.05)], [int(sh*0.9), int(sw*0.95)]]
    walls = [list(range(box[0][0], box[1][0]+1)),
             list(range(box[0][0], box[0][1]+1)),
             list(range(box[1][0], box[1][1]+1)),
             list(range(box[0][1], box[1][1]+1))]
    print(box)
    print(walls)
    
    #paddles position
    player= [box[1][0]//2, box[0][1]+2]
    comp = [box[1][0]//2, box[1][1]-2]
    
    #ball position
    ball = [box[1][0]//2+2, box[1][1]//2+1]
    
    ball_speed = 100
    
    direction = 1
    
    while True:
        stdscr.clear()
        draw_board(stdscr, box)
        draw_paddle(stdscr, box, player[0], player[1])
        draw_paddle(stdscr, box, comp[0], comp[1])
        draw_ball(stdscr, walls, ball, ball_speed, player, comp, direction)
        #print(ball)
        key = stdscr.getch()
        if key == curses.KEY_UP and player[0] > box[0][0]+1:
            player[0] -= 1
        elif key == curses.KEY_DOWN and player[0] < (box[1][0] - 6):
            player[0] += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            break
        
curses.wrapper(main)