import curses, sys, random, time, threading
import numpy as np

from methods.menus import *
import main_menu
import leaderboard

"""
add winning row line
"""

# infinity
INF = float("inf")

#grid size
size = 3

m_menu = ['1 player', '2 player', 'Return home']
botmenu = ['Easy', 'Medium', 'Hard']
s_menu = ['Play again', 'Save score', 'Return home']
        
#choose bot difficulty        
def bot_opt(stdscr, selected_row):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    
    title = "Bot difficulty"
    
    x = width//2 +2
    y = height//2 -1
    
    stdscr.addstr(y-2, x - len(title)//2-1, title, curses.A_STANDOUT)
    
    left = '►'
    right = '◄'
    
    diff = botmenu[selected_row]
    
    stdscr.addstr(y, x-len(diff)//2-2, right+diff+left, curses.A_BOLD)
       
    stdscr.refresh()
        
#This function is used to draw the board
def draw_board(stdscr):
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    x = width//2 -10
    y = height//2 - 5
    
    size_x = 16
    
    stdscr.addstr(y - 3, x-10, str(' ')*(size_x)+'│'+str(' ')*(size_x)+'│'+str(' ')*(size_x))
    stdscr.addstr(y - 2, x-10, str(' ')*(size_x)+'│'+str(' ')*(size_x)+'│'+str(' ')*(size_x))
    stdscr.addstr(y - 1, x-10, str(' ')*(size_x)+'│'+str(' ')*(size_x)+'│'+str(' ')*(size_x))
    stdscr.addstr(y    , x-10, str(' ')*(size_x)+'│'+str(' ')*(size_x)+'│'+str(' ')*(size_x))
    stdscr.addstr(y + 1, x-10, str(' ')*(size_x)+'│'+str(' ')*(size_x)+'│'+str(' ')*(size_x))
    stdscr.addstr(y + 2, x-10, str('─')*(size_x)+'┼'+str('─')*(size_x)+'┼'+str('─')*(size_x))
    stdscr.addstr(y + 3, x-10, str(' ')*(size_x)+'│'+str(' ')*(size_x)+'│'+str(' ')*(size_x))
    stdscr.addstr(y + 4, x-10, str(' ')*(size_x)+'│'+str(' ')*(size_x)+'│'+str(' ')*(size_x))
    stdscr.addstr(y + 5, x-10, str(' ')*(size_x)+'│'+str(' ')*(size_x)+'│'+str(' ')*(size_x))
    stdscr.addstr(y + 6, x-10, str(' ')*(size_x)+'│'+str(' ')*(size_x)+'│'+str(' ')*(size_x))
    stdscr.addstr(y + 7, x-10, str(' ')*(size_x)+'│'+str(' ')*(size_x)+'│'+str(' ')*(size_x))
    stdscr.addstr(y + 8, x-10, str('─')*(size_x)+'┼'+str('─')*(size_x)+'┼'+str('─')*(size_x))
    stdscr.addstr(y + 9, x-10, str(' ')*(size_x)+'│'+str(' ')*(size_x)+'│'+str(' ')*(size_x))
    stdscr.addstr(y +10, x-10, str(' ')*(size_x)+'│'+str(' ')*(size_x)+'│'+str(' ')*(size_x))
    stdscr.addstr(y +11, x-10, str(' ')*(size_x)+'│'+str(' ')*(size_x)+'│'+str(' ')*(size_x))
    stdscr.addstr(y +12, x-10, str(' ')*(size_x)+'│'+str(' ')*(size_x)+'│'+str(' ')*(size_x))
    stdscr.addstr(y +13, x-10, str(' ')*(size_x)+'│'+str(' ')*(size_x)+'│'+str(' ')*(size_x))
    
#draw the score
def print_score(stdscr, score_pl1, score_pl2, bot):
    height, width = stdscr.getmaxyx()
    
    s_x = width//2
    s_y = 3
    
    stdscr.addstr(s_y, s_x-14, 'Player 1: {}'.format(score_pl1), curses.A_BOLD)
    
    if bot:
        stdscr.addstr(s_y, s_x+14, 'AI: {}'.format(score_pl2), curses.A_BOLD)
    else:
        stdscr.addstr(s_y, s_x+14, 'Player 2: {}'.format(score_pl2), curses.A_BOLD)

def move_(grid, row, col, player):
    grid[row][col] = player

def undo(grid, row, col):
    grid[row][col] = 0

def empt_grid(grid):
    for i in grid:
        if i != ' ':
            return False
    return True

def win_player(grid, char):
    # check if a player wins the game
    # check for rows, columns and diagonals
    result = char * size in grid.sum(axis=1)
    result = result or char * size in grid.sum(axis=0)
    result = result or char * size == np.trace(grid)
    result = result or char * size == np.trace(np.fliplr(grid))
    return result

def terminal(grid):
    # check if the game is at a terminal state
    # a game is a terminal state if either player wins or it's a tie
    return win_player(grid, -1) or win_player(grid, 1) or 0 not in grid

def utility(grid):
    # return the score corresponding to the terminal state
    if win_player(grid, -1):
        return -1
    if win_player(grid, 1):
        return 1
    return 0

def actions(grid):
    # return possible actions a player can take at each state
    result = np.where(grid == 0)
    result = np.transpose(result)
    np.random.shuffle(result)
    return result

def minimax(grid, computer, alpha, beta, depth):
    max_depth = INF
    
    if difficulty == 0:
        max_depth = 1
    elif difficulty == 1:
        max_depth = 5
        
    # return the maximum value a player can obtain at each step
    if terminal(grid):
        return utility(grid), depth
    
    if computer:
        func = max
        m = -INF
        char = 1
    else:
        func = min
        m = INF
        char = -1

    for action in actions(grid):
        row, col = action
        move_(grid, row, col, char)
        if depth <= max_depth:
            value, depth = minimax(grid, not computer, alpha, beta, depth + 1)
            m = func(m, value)
        # undo the move
        undo(grid, row, col)
        # alpha-beta pruning
        if computer:
            alpha = func(alpha, m)
        else:
            beta = func(beta, m)

        if beta <= alpha:
            break

    return m, depth

def best_move(grid):
    # find all empty cells and compute the minimax for each one
    m = alpha = -INF
    d = beta = INF
    for action in actions(grid):
        row, col = action
        move_(grid, row, col, 1)
        value, depth = minimax(grid, False, alpha, beta, 0)
        if value > m or (value == m and depth < d):
            result = row, col
            m = value
            d = depth
        # undo the move
        undo(grid, row, col)
    return result
            
def bot_mainloop(stdscr, grid, player_turn, difficulty, moves):
    #players
    playerX = 'X'
    playerO = 'O'
    
    #opt for moves list
    pos_x = 0
    pos_y = 0
    
    #exit menu
    exit_row = 1
    
    win = None
    
    height, width = stdscr.getmaxyx()
    
    if difficulty == 2: player_turn = 0
    
    while True:
        if player_turn:
            curses.curs_set(1)
            stdscr.move(moves[0][pos_y], moves[1][pos_x])
        
            key = stdscr.getch()
            
            if key == curses.KEY_UP and pos_y > 0:
                pos_y -= 1
            elif key == curses.KEY_DOWN and pos_y < 2:
                pos_y += 1
            elif key == curses.KEY_LEFT and pos_x > 0:
                pos_x -= 1
            elif key == curses.KEY_RIGHT and pos_x < 2:
                pos_x += 1
            elif key == curses.KEY_EXIT or key == 27:
                while True:
                    curses.curs_set(0)
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
                            
            elif key == curses.KEY_ENTER or key in [10, 13]:
                #get cursor position
                y, x = curses.getsyx()
            
                #if cursor posiion == ' ' print player
                if stdscr.inch(y, x) == 32:
                    stdscr.addch(y, x, playerX)
                    
                    #update the board's current state every time the user turn arrives. 
                    grid[pos_x][pos_y] = -1
                    
                    if win_player(grid, -1):
                        curses.curs_set(0)
                        stdscr.addstr(height//2, width//2-len('YOU WON !')//2, 'YOU WON !'+5, curses.A_STANDOUT)
                        stdscr.timeout(-1)
                        stdscr.getch()
                        win = True
                        break
                        
                    if terminal(grid):
                        curses.curs_set(0)
                        stdscr.addstr(height//2, width//2-len('TIE !')//2+5, 'TIE !', curses.A_STANDOUT)
                        stdscr.timeout(-1)
                        stdscr.getch()
                        break
                
                    #change player turn
                    player_turn = (player_turn + 1) % 2
                    
                    curses.curs_set(0)
                
        else:        
            #get compt move
            row, col = best_move(grid)
            move_(grid, row, col, 1)
            y, x = moves[0][col], moves[1][row]
            
            #move cursor
            stdscr.move(y, x)
            stdscr.addch(y, x, playerO)
            
            # check if the computer wins
            if win_player(grid, 1):
                curses.curs_set(0)
                stdscr.addstr(height//2, width//2-len('YOU LOST !')//2+5, 'YOU LOST !', curses.A_STANDOUT)
                stdscr.timeout(-1)
                stdscr.getch()
                win = False
                break
            
            if terminal(grid):
                curses.curs_set(0)
                stdscr.addstr(height//2, width//2-len('TIE !')//2+5, 'TIE !', curses.A_STANDOUT)
                stdscr.timeout(-1)
                stdscr.getch()
                break
                
            #change player turn
            player_turn = (player_turn + 1) % 2
    
    return win

def two_players(stdscr, grid, player_turn, moves):
    curses.curs_set(1)
    
    #players
    playerX = 'X'
    playerO = 'O'
    
    #opt for moves list
    pos_x = 0
    pos_y = 0
    
    #exit menu
    exit_row = 1
    
    #draw the board every time a game starts
    draw_board(stdscr)
    
    #draw the score
    print_score(stdscr, score_pl1, score_pl2, False)
    
    win = None
    
    while True:
        stdscr.move(moves[0][pos_y], moves[1][pos_x])
        
        key = stdscr.getch()
        
        if key == curses.KEY_UP and pos_y > 0:
            pos_y -= 1
        elif key == curses.KEY_DOWN and pos_y < 2:
            pos_y += 1
        elif key == curses.KEY_LEFT and pos_x > 0:
            pos_x -= 1
        elif key == curses.KEY_RIGHT and pos_x < 2:
            pos_x += 1
        elif key == curses.KEY_EXIT or key == 27:
            while True:
                curses.curs_set(0)
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
        elif key == curses.KEY_ENTER or key in [10, 13]:
            #get cursor position
            y, x = curses.getsyx()
                
            #if cursor posiion == ' ' print player
            if stdscr.inch(y, x) == 32:
                stdscr.addch(y, x, playerO if player_turn else playerX)
                
                #change player turn
                player_turn = (player_turn + 1) % 2
        
                #update the board's current state every time the user turn arrives. 
                grid[pos_y][pos_x] = -1 if player_turn else 1
            
            #check if grid
            curses.curs_set(0)
            height, width = stdscr.getmaxyx()

            if win_player(grid, -1):
                stdscr.addstr(height//2, width//2-len('PLAYER 1 WON !')//2+5, 'PLAYER 1 WON !', curses.A_STANDOUT)
                stdscr.timeout(-1)
                stdscr.getch()
                win = True
                break
            
            if terminal(grid):
                stdscr.addstr(height//2, width//2-len('TIE !')//2+5, 'TIE !', curses.A_STANDOUT)
                stdscr.timeout(-1)
                stdscr.getch() 
                break
            
            if win_player(grid, 1):
                stdscr.addstr(height//2, width//2-len('PLAYER 2 WON !')//2+5, 'PLAYER 2 WON !', curses.A_STANDOUT)
                stdscr.timeout(-1)
                stdscr.getch()
                win = False 
                break   
                
            curses.curs_set(1)
            
    return win
    
#mainloop
def main(stdscr):
    global score_pl1, score_pl2, difficulty
    
    stdscr.clear()
    curses.curs_set(0)
    
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    
    #main menu
    selected_row = 0
    #sub menu
    current_row = 0
    #exit menu
    exit_row = 1
    #bot menu
    bot_row = 2
    
    #player turn
    player_turn = 1
    
    #score for each player
    try:
        score_pl1 = score_pl1
    except:
        score_pl1 = 0
        
    try:
        score_pl2 = score_pl2
    except:    
        score_pl2 = 0
    
    height, width = stdscr.getmaxyx()

    x = width//2 -10
    y = height//2 - 5
    
    #position where the player(s)/ai can move
    moves = [[y-1, y+5, y+11], [x-2, x+14, x+30]]
    
    #game board
    grid = np.zeros((size, size), int)
    
    #cond to see if two player or one player
    bot = None
    
    #bot difficulty
    difficulty = 2
    
    #print main menu
    menu(stdscr, selected_row, m_menu, "Tic tac toe:")
    
    game_counter = 0
    
    while True:
        key = stdscr.getch()
        
        stdscr.clear()
        
        if key == curses.KEY_UP and selected_row > 0:
            selected_row -= 1
        elif key == curses.KEY_DOWN and selected_row < len(m_menu)-1:
            selected_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if selected_row == 0:
                bot = True
                bot_opt(stdscr, bot_row)
                while True:
                    key = stdscr.getch()
        
                    stdscr.clear()
                    
                    if key == curses.KEY_LEFT and bot_row > 0:
                        bot_row -= 1
                    elif key == curses.KEY_RIGHT and bot_row < len(botmenu)-1:
                        bot_row += 1
                    elif key == curses.KEY_EXIT or key == 27:
                        break
                    elif key == curses.KEY_ENTER or key in [10, 13]:

                        while True:
                            if (score_pl2 > 0 or score_pl1 > 0) or game_counter > 0:
                                
                                curses.curs_set(0)
                                menu(stdscr, current_row, s_menu, "Tic tac toe:")
                                
                                while True:
                                    key = stdscr.getch()
                    
                                    stdscr.clear()
                                    
                                    if key == curses.KEY_UP and current_row > 0:
                                        current_row -= 1
                                    elif key == curses.KEY_DOWN and current_row < len(s_menu)-1:
                                        current_row += 1
                                    elif key == curses.KEY_ENTER or key in [10, 13]:
                                        if current_row == 0:
                                            grid = np.zeros((size, size), int)                                            
                                            break
                                        elif current_row == 1:
                                            name_player = leaderboard.text_entry()
                                            leaderboard.save_score(name = name_player, snake_score = score)
                                            main_menu.run_app()
                                        elif current_row == 2:
                                            main_menu.run_app()
                                    menu(stdscr, current_row, s_menu, "Tic tac toe:")

                            difficulty = bot_row
                            
                            
                            #draw the board every time a game starts
                            drw0 = threading.Thread(target = draw_board, args = (stdscr,))
                            #draw the score
                            drw1 = threading.Thread(target = print_score, args = (stdscr, score_pl1, score_pl2, True,))
                            
                            drw0.start()
                            drw1.start()
                            
                            while True:
                                if not drw0.is_alive():
                                    break
                            #mainloop
                            bot_parametre = bot_mainloop(stdscr, grid, player_turn, difficulty, moves)
                            
                            if bot_parametre:
                                score_pl1 += 1
                            elif bot_parametre == False:
                                score_pl2 += 1
                            else:
                                game_counter +=1
                            #break
                        
                    bot_opt(stdscr, bot_row)                        
            elif selected_row == 1:
                if (score_pl2 > 0 or score_pl1 > 0) or game_counter > 0:
                    
                    curses.curs_set(0)
                    menu(stdscr, current_row, s_menu, "Tic tac toe:")
                    
                    while True:
                        key = stdscr.getch()
        
                        stdscr.clear()
                        
                        if key == curses.KEY_UP and current_row > 0:
                            current_row -= 1
                        elif key == curses.KEY_DOWN and current_row < len(s_menu)-1:
                            current_row += 1
                        elif key == curses.KEY_ENTER or key in [10, 13]:
                            if current_row == 0:
                                grid = np.zeros((size, size), int)
                                break
                            elif current_row == 1:
                                name_player = leaderboard.text_entry()
                                leaderboard.save_score(name = name_player, snake_score = score)
                                main_menu.run_app()
                            elif current_row == 2:
                                main_menu.run_app()
                        menu(stdscr, current_row, s_menu, "Tic tac toe:")
                            
                hum_parametre = two_players(stdscr, grid, player_turn, moves)
                
                if hum_parametre:
                    score_pl1 += 1
                elif hum_parametre == False:
                    score_pl2 += 1
                else:
                    game_counter +=1
                    
            elif selected_row == 2:
                main_menu.run_app()
                
        menu(stdscr, selected_row, m_menu, "Tic tac toe:")
        
def xo_start():        
    curses.wrapper(main)      