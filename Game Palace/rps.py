import random, sys, curses, threading, time

import main_menu
import leaderboard
from methods.menus import *


scissors=["                                             ▓▓▓▓▓▓         ",           
          "                                          ▓▓▓▓░░░░▓▓        ",            
          "                                         ▓▓░░░░░░▓▓         ",            
          "       ██████████                      ▓▓░░░░░░▓▓           ",             
          "     ██▓▓▓▓▓▓▓▓▓▓██                  ▓▓░░░░░░▓▓             ",             
          "   ██▓▓▓▓██████▓▓▓▓██              ▓▓░░░░░░▓▓               ",             
          " ██▓▓▓▓██      ██▓▓▓▓██          ▓▓░░░░░░▓▓                 ",             
          " ██▓▓▓▓██        ██▓▓▓▓██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ",              
          " ██▓▓▓▓▓▓████████▓▓▓▓▓▓▓▓██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▓▓ ",             
          "   ██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██░░██░░░░░░░░░░░░░░░░░░░░░░▓▓▓▓   ",             
          "     ██████████████████████░░░░░░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓       ",             
          "                   ████▓▓▓▓██░░▓▓                           ",             
          "                 ██▓▓▓▓▓▓▓▓▓▓██                             ",             
          "               ██▓▓▓▓████▓▓▓▓██                             ",             
          "             ██▓▓▓▓██    ██▓▓██                             ",             
          "           ██▓▓▓▓██      ██▓▓██                             ",             
          "         ██▓▓▓▓██      ██▓▓▓▓██                             ",             
          "         ██▓▓██      ██▓▓▓▓██                               ",             
          "         ██▓▓▓▓██████▓▓▓▓██                                 ",             
          "           ██▓▓▓▓▓▓▓▓▓▓██                                   ",             
          "             ██████████                                     "]

rev_scissors = [i[::-1] for i in scissors]

paper = ["                                              ░░░░           ",
         "                         ░░░░                  ░░            ",
         "                     ░░░░                    ░░░░            ",
         "                   ░░░░░░                  ░░░░              ",
         "                   ░░░░░░                ░░░░          ░░    ",
         "                   ░░░░                ░░░░░░        ░░▒▒░░  ",
         "                   ░░░░              ░░░░░░        ░░░░░░░░  ",
         "                   ▒▒░░░░          ░░░░░░░░    ░░░░░░░░░░    ",
         "                 ░░░░░░░░          ░░░░░░    ░░░░░░░░        ",
         "                 ░░░░░░░░        ░░░░░░    ░░░░░░░░      ░░  ",
         "                 ▒▒░░        ░░░░░░      ░░░░░░░░    ░░░░░░░░",
         "                 ░░░░  ░░░░░░░░░░░░    ░░▒▒░░░░    ░░▒▒░░░░░░",
         "               ░░░░    ░░░░░░░░░░░░░░░░  ░░░░  ░░▒▒░░░░░░    ",
         "               ▒▒░░░░░░░░░░░░░░░░░░░░░░░░  ░░░░░░▒▒░░        ",
         "               ▒▒░░░░░░░░░░░░░░░░░░░░░░░░  ▒▒░░░░            ",
         "              ▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░  ░░░░░░░░░░░░   ",
         "              ▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒░░░░░░░░░░░░ ",
         "              ▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒░░░░░░░░░░░░ ",
         "            ▒▒▒▒▒▒░░░░░░░░    ░░░░░░░░░░░░░░░░░░             ",
         "        ░░▓▓▒▒▒▒▒▒░░░░░░        ░░░░░░░░                     ",
         "      ░░▓▓▒▒▒▒░░░░▒▒░░░░░░░░░░░░░░░░░░                       ",
         "    ░░▒▒▒▒░░░░▒▒░░▒▒░░░░░░░░░░░░░░                           ",
         "  ░░░░░░▒▒░░░░░░░░░░░░░░░░░░░░░░                             ",
         "░░▒▒░░░░░░░░░░░░░░░░░░░░░░                                   "]

rev_paper = [i[::-1] for i in paper]

rock = ["                                      ████  ████████                ",
        "                                    ██░░░░██░░░░░░░░██              ",
        "                                  ▓▓░░░░░░░░▓▓░░░░░░░░██▓▓          ",
        "                                ██░░░░░░░░░░░░██░░░░██░░░░██        ",
        "                              ▓▓░░░░░░░░██░░░░░░▓▓▓▓░░░░░░██        ",
        "                            ▓▓░░░░░░░░░░██░░░░░░░░██░░░░░░██▓▓      ",
        "                         ██░░░░░░░░░░░░██░░░░░░░░░░██░░██░░░░██     ",
        "                        ██░░░░░░░░░░░░██░░████░░░░░░████░░░░░░██    ",
        "                        ██░░░░░░░░████░░░░██░░████████░░░░░░░░████  ",
        "                      ██░░░░░░░░░░░░░░████░░░░░░░░██░░░░░░░░██░░░░██",
        "                      ██░░░░░░░░░░░░░░██░░██░░░░██░░░░░░░░██░░░░░░██",
        "                    ██░░░░░░░░░░░░░░░░░░██░░████░░░░░░░░██░░░░░░████",
        "                    ██░░░░░░░░░░░░░░░░░░██░░░░░░██░░░░██░░░░░░██░░██",
        "                    ██░░░░░░░░░░░░░░░░░░██░░░░░░░░████░░░░░░██░░██  ",
        "                  ██░░░░░░░░░░░░░░░░░░░░██░░░░░░░░░░░░▓▓██▓▓░░▓▓    ",
        "                  ██░░░░░░░░░░░░░░░░░░██░░░░░░░░░░░░░░░░░░░░▓▓      ",
        "                  ██░░░░░░░░░░░░░░░░░░██░░░░░░░░░░░░░░░░░░██        ",
        "                ██░░░░░░░░░░░░░░░░░░██░░░░░░░░░░░░░░░░░░██          ",
        "              ██░░░░░░░░░░░░░░░░░░▓▓░░░░░░░░░░░░░░░░████            ",
        "            ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██                ",
        "          ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░████                  ",
        "        ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▓▓██                      ",
        "      ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██                          ",
        "    ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██                            ",
        "  ▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██                            "]

rev_rock = [i[::-1] for i in rock]

                   
countdown_0 = ["      000000000     ",
               "    00:::::::::00   ",
               "  00:::::::::::::00 ",
               " 0:::::::000:::::::0",
               " 0::::::0   0::::::0",
               " 0:::::0     0:::::0",
               " 0:::::0     0:::::0",
               " 0:::::0 000 0:::::0",
               " 0:::::0 000 0:::::0",
               " 0:::::0     0:::::0",
               " 0:::::0     0:::::0",
               " 0::::::0   0::::::0",
               " 0:::::::000:::::::0",
               "  00:::::::::::::00 ",
               "    00:::::::::00   ",
               "      000000000     "]

              
        
countdown_1 = ["  1111111    ",
               "  1::::::1   ",
               " 1:::::::1   ",
               " 111:::::1   ",
               "    1::::1   ",
               "    1::::1   ",
               "    1::::1   ",
               "    1::::l   ",
               "    1::::l   ",
               "    1::::l   ",
               "    1::::l   ",
               "    1::::l   ",
               " 111::::::111",
               " 1::::::::::1",
               " 1::::::::::1",
               " 111111111111"]
            
            
            
countdown_2 = ["  222222222222222    ",
               " 2:::::::::::::::22  ",
               " 2::::::222222:::::2 ",
               " 2222222     2:::::2 ",
               "             2:::::2 ",
               "             2:::::2 ",
               "          2222::::2  ",
               "     22222::::::22   ",
               "   22::::::::222     ",
               "  2:::::22222        ",
               " 2:::::2             ",
               " 2:::::2             ",
               " 2:::::2       222222",
               " 2::::::2222222:::::2",
               " 2::::::::::::::::::2",
               " 22222222222222222222"]

countdown_3 = ["  333333333333333   ",
               " 3:::::::::::::::33 ",
               " 3::::::33333::::::3",
               " 3333333     3:::::3",
               "             3:::::3",
               "             3:::::3",
               "     33333333:::::3 ",
               "     3:::::::::::3  ",
               "     33333333:::::3 ",
               "             3:::::3",
               "             3:::::3",
               "             3:::::3",
               " 3333333     3:::::3",
               " 3::::::33333::::::3",
               " 3:::::::::::::::33 ",
               "  333333333333333   "]

num_dict = {'4': countdown_3, '3': countdown_2, '2': countdown_1, '1': countdown_0}

moves = ['rock', 'paper', 'scissors']

def rand():
    return random.choice(moves)

def win_lost(playerMove, rnd):
    #rnd = rand()
    #if rnd == player choice its tie
    if rnd == playerMove:
        return 'Tie !'
    #check paper
    elif playerMove == 'paper':
        if rnd == 'scissors':
            return 'You lost'
        else:
            return 'You won'
    #check rock
    elif playerMove == 'rock':
        if rnd == 'paper':
            return 'You lost'
        else:
            return 'You won'
    #check scissors
    elif playerMove == 'scissors':
        if rnd == 'rock':
            return 'You lost'
        else:
            return 'You won'

#draw rock, paper, scissors
def draw_ascii(stdscr, playerMove, score_player, score_computer, rnd):
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    x = width//2
    y = height//2 - 5
    
    rev_val = []
    
    if rnd == 'rock':
        rev_val = rev_rock
    elif rnd == 'paper':
        rev_val = rev_paper
    elif rnd == 'scissors':
        rev_val = rev_scissors
    
    state = win_lost(playerMove, rnd)
    
    if playerMove == 'rock':
        #print choice
        for i in range(len(rock)):
            stdscr.addstr(y+i, width//2-(len(rock[0])+5), rock[i])
        #print computer choice
        for i in range(len(rev_val)):
            stdscr.addstr(y+i, width//2+14, rev_val[i])
    elif playerMove == 'paper':
        for i in range(len(paper)):
            stdscr.addstr(y+i, width//2-(len(paper[0])+5), paper[i])
        for i in range(len(rev_val)):
            stdscr.addstr(y+i, width//2+14, rev_val[i])
    elif playerMove == 'scissors':
        for i in range(len(scissors)):
            stdscr.addstr(y+i, width//2-(len(scissors[0])+5), scissors[i])
        for i in range(len(rev_val)):
            stdscr.addstr(y+i, width//2+14, rev_val[i])
            
    stdscr.addstr(y-10, x-len(state)//2, state, curses.A_STANDOUT)
        
    stdscr.refresh()

def print_score(stdscr, score_player, score_computer):
    height, width = stdscr.getmaxyx()
    
    s_x = width//2
    s_y = 3
    
    stdscr.addstr(s_y, s_x-14, 'Player : {}'.format(score_player), curses.A_BOLD)
    
    stdscr.addstr(s_y, s_x+14, 'Computer : {}'.format(score_computer), curses.A_BOLD)
        
def draw_countdown(stdscr):
    stdscr.clear()
    
    height, width = stdscr.getmaxyx()
    
    t=4
    
    while t:
        stdscr.erase()
        x = width//2
        y = height//2
        if t == 4:
            y -= len(countdown_3)//2
            x -= len(countdown_3[0])//2
            for i in range(len(countdown_3)):
                stdscr.addstr(y+i, x, countdown_3[i])
        elif t == 3:
            y -= len(countdown_2)//2
            x -= len(countdown_2[0])//2
            for i in range(len(countdown_2)):
                stdscr.addstr(y+i, x, countdown_2[i])
        elif t == 2:
            y -= len(countdown_1)//2
            x -= len(countdown_1[0])//2
            for i in range(len(countdown_1)):
                stdscr.addstr(y+i, x, countdown_1[i])
        elif t == 1:
            y -= len(countdown_0)//2
            x -= len(countdown_0[0])//2
            for i in range(len(countdown_0)):
                stdscr.addstr(y+i, x, countdown_0[i])
        stdscr.refresh()
        time.sleep(1) 
        t -= 1
    stdscr.clear()
    
#exit_event = threading.Event()

def start_countdown(stdscr):
    curses.curs_set(0)
    thc = threading.Thread(target = draw_countdown, args = (stdscr,))
    
    thc.start()
    
    key = stdscr.getch()
    
    while True:
        if not thc.is_alive():
            break
        elif key == curses.KEY_EXIT or key == 27:
            return True
        
    return True


    
def choose(stdscr, current_row):
    stdscr.clear()
    
    #window x, y
    height, width = stdscr.getmaxyx()
    
    for i in range(len(rock)):
            stdscr.addstr(height//4+i, 5, rock[i])
    for i in range(len(paper)):
            stdscr.addstr(height//4+i, width//2-(len(paper[0])//2), paper[i])
    for i in range(len(scissors)):
            stdscr.addstr(height//3+i, width//2+(len(scissors[0])//2+10), scissors[i])
    
    x = width//2
    
    for index, row in enumerate(['ROCK', 'PAPER', 'SCISSORS']):
            
        x -= len(['ROCK', 'PAPER', 'SCISSORS']) + 5
        y = height - 5
        
        if index == current_row:
            if index == 1:
                stdscr.addstr(y, x, row, curses.color_pair(1))
            else:
                stdscr.addstr(y, x, row, curses.color_pair(1))
        else:
            if index == 1:
                stdscr.addstr(y, x, row, curses.A_BOLD)
            else:
                stdscr.addstr(y, x, row, curses.A_BOLD)
        
        x += len(row)+ 10
            
        stdscr.refresh()

m_menu = ['Play', 'Save Score', 'Return Home']

def main(stdscr):
    curses.curs_set(0)
    
    #set color pair
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    
    current_row = 0
    selected_row = 0
    
    score_player = 0
    score_computer = 0
    
    while True:
        while True:
            stdscr.clear()
            menu(stdscr, selected_row, m_menu, 'RPS :')
            key = stdscr.getch()
            if key == curses.KEY_UP and selected_row > 0:
                selected_row -= 1
            elif key == curses.KEY_DOWN and selected_row < len(m_menu)-1:
                selected_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                if selected_row == 0:
                    choose(stdscr, current_row)
                    print_score(stdscr, score_player, score_computer)
                    while True:
                        playerMove = None
                        
                        key = stdscr.getch()
                        
                        stdscr.erase()
                        
                        if key == curses.KEY_LEFT and current_row > 0:
                            current_row -= 1
                        elif key == curses.KEY_RIGHT and current_row < 2:
                            current_row += 1
                        elif key == curses.KEY_EXIT or key == 27:
                            main(stdscr)
                        elif key == curses.KEY_ENTER or key in [10, 13]:    
                            if current_row == 0:
                                playerMove = 'rock'
                                if start_countdown(stdscr):
                                    rnd = rand()
                                    draw_ascii(stdscr, playerMove, score_player, score_computer, rnd)
                                    if win_lost(playerMove, rnd) == 'You won': score_player+=1
                                    elif win_lost(playerMove, rnd) == 'You lost': score_computer+=1
                                    print_score(stdscr, score_player, score_computer)
                                    stdscr.timeout(-1)
                                    stdscr.getch()
                            if current_row == 1:
                                playerMove = 'paper'
                                if start_countdown(stdscr):
                                    rnd = rand()
                                    draw_ascii(stdscr, playerMove, score_player, score_computer, rnd)
                                    if win_lost(playerMove, rnd) == 'You won': score_player+=1
                                    elif win_lost(playerMove, rnd) == 'You lost': score_computer+=1
                                    print_score(stdscr, score_player, score_computer)
                                    stdscr.timeout(-1)
                                    stdscr.getch()
                            if current_row == 2:
                                playerMove = 'scissors'
                                if start_countdown(stdscr):
                                    rnd = rand()
                                    draw_ascii(stdscr, playerMove, score_player, score_computer, rnd)
                                    if win_lost(playerMove, rnd) == 'You won': score_player+=1
                                    elif win_lost(playerMove, rnd) == 'You lost': score_computer+=1
                                    print_score(stdscr, score_player, score_computer)
                                    stdscr.timeout(-1)
                                    stdscr.getch()     
                        
                        choose(stdscr, current_row)
                        print_score(stdscr, score_player, score_computer)
                elif selected_row == 1:
                    name_player = leaderboard.text_entry()
                    leaderboard.save_score(name = name_player, rps_score = score_player)
                    main_menu.run_app()
                elif selected_row == 2:
                    main_menu.run_app()
def rps_start():
    curses.wrapper(main)