import curses, random, sys, time
from curses import textpad

import main_menu
import leaderboard
from methods.menus import *


OPPOSITE_DIRECTION_DICT = {
    curses.KEY_UP: curses.KEY_DOWN,
    curses.KEY_DOWN: curses.KEY_UP,
    curses.KEY_RIGHT: curses.KEY_LEFT,
    curses.KEY_LEFT: curses.KEY_RIGHT
}

DIRECTIONS_LIST = [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_DOWN, curses.KEY_UP]


def create_food(snake_body, box):
    """Simple function to find coordinates of food which is inside box and not on snake_body body"""
    food = None
    while food is None:
        food = [random.randint(box[0][0]+1, box[1][0]-1), 
        random.randint(box[0][1]+1, box[1][1]-1)]
        if food in snake_body:
            food = None
    return food

s_menu = ['Play again', 'Save Score', 'Return Home']

def main(stdscr):
    # initial settings
    stdscr.clear()
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(125)
    
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    
    speed=0
    
    exit_row = 1
    s_menu_row = 0
    
    # create a game box
    sh, sw = stdscr.getmaxyx()
    box = [[int(sh*0.15), int(sw*0.05)], [int(sh-3), int(sw*0.95)]]  # [[ul_y, ul_x], [dr_y, dr_x]]
    textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])

    # create snake_body and set initial direction
    snake_body = [[sh//2, sw//2+1], [sh//2, sw//2], [sh//2, sw//2-1]]
    direction = curses.KEY_RIGHT

    # draw snake_body
    for y,x in snake_body:
        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(y, x, '@')
        stdscr.attroff(curses.color_pair(2))

    # create food
    food = create_food(snake_body, box)
    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(food[0], food[1], '*')
    stdscr.attroff(curses.color_pair(3))

    # print score
    score = 0
    score_text = "Score: {}".format(score)
    stdscr.addstr(2, sw//2 - len(score_text)//2, score_text, curses.A_STANDOUT)

    while True:
        # non-blocking input
        key = stdscr.getch()

        # set direction if user pressed any arrow key and that key is not opposite of current direction
        if key in DIRECTIONS_LIST and key != OPPOSITE_DIRECTION_DICT[direction]:
            direction = key

        # find next position of snake_body head
        head = snake_body[0]
        if key == curses.KEY_EXIT or key == 27:
            while True:
                quit_menu(stdscr, exit_row)
                key = stdscr.getch()
                if key == curses.KEY_LEFT and exit_row > 0:
                    exit_row -= 1
                elif key == curses.KEY_RIGHT and exit_row < 1:
                    exit_row += 1
                elif key == curses.KEY_ENTER or key in [10, 13]:
                    if exit_row == 1:
                        stdscr.clear()
                        main(stdscr)
                        break
                    else:
                        sys.exit()
                
        elif direction == curses.KEY_RIGHT:
            new_head = [head[0], head[1]+1]
        elif direction == curses.KEY_LEFT:
            new_head = [head[0], head[1]-1]
        elif direction == curses.KEY_DOWN:
            new_head = [head[0]+1, head[1]]
        elif direction == curses.KEY_UP:
            new_head = [head[0]-1, head[1]]

        # insert and print new head
        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(new_head[0], new_head[1], ' ')
        stdscr.attroff(curses.color_pair(2))
        snake_body.insert(0, new_head)

        # if sanke head is on food
        if snake_body[0] == food:
            # update score
            score += 1
            score_text = "Score: {}".format(score)
            stdscr.addstr(2, sw//2 - len(score_text)//2, score_text, curses.A_STANDOUT)

            # create new food
            food = create_food(snake_body, box)
            stdscr.attron(curses.color_pair(3))
            stdscr.addstr(food[0], food[1], '*')
            stdscr.attroff(curses.color_pair(3))

            # increase speed of game
            speed += 3
            if speed > 90:
                stdscr.timeout(30)
            else:
                stdscr.timeout(125 - speed)
        else:
            # shift snake_body's tail
            stdscr.addstr(snake_body[-1][0], snake_body[-1][1], " ")
            snake_body.pop()

        # conditions for game over
        if (snake_body[0][0] in [box[0][0], box[1][0]] or 
            snake_body[0][1] in [box[0][1], box[1][1]] or 
            snake_body[0] in snake_body[1:]):
            msg = "Game Over!"
            stdscr.addstr(sh//2, sw//2-len(msg)//2, msg, curses.A_BOLD)
            stdscr.timeout(-1) 
            stdscr.getch()
            while True:
                stdscr.clear()
                menu(stdscr, s_menu_row, s_menu, "SNAKE:")
                key = stdscr.getch()
                if key == curses.KEY_UP and s_menu_row > 0:
                    s_menu_row -= 1
                elif key == curses.KEY_DOWN and s_menu_row < len(s_menu)-1:
                    s_menu_row += 1
                elif key == curses.KEY_ENTER or key in [10, 13]:
                    if s_menu_row == 0:
                        stdscr.clear()
                        main(stdscr)
                    elif s_menu_row == 1:
                        name_player = leaderboard.text_entry()
                        leaderboard.save_score(name = name_player, snake_score = score)
                        main_menu.run_app()
                    elif s_menu_row == 2:
                        main_menu.run_app()
            else:break
        
        stdscr.refresh()

def snake_start():
    curses.wrapper(main)