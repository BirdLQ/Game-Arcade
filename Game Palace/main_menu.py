import curses, time, random, sys, win32console, locale, threading
from pygame import mixer

#games
from methods.menus import *
import rps
import snake
import leaderboard
import asciiAnimation
import snow
import xo

#set encodage to utf-8
locale.setlocale(locale.LC_ALL, '')

#set window title
win32console.SetConsoleTitle('Game Palace')

#play music
def music_player():
    mixer.init()
    mixer.music.load('music/theme3.mp3')
    mixer.music.play(-1)

th1 = threading.Thread(target = music_player)

th1.start()


'''
TO ADD:

exit full sceen to windowed
    
mixer.pause
mixer.unpause
mixer.set_volume(0.7)

game name wave effect
'''

#main menu
m_menu = ['Play', 'Games list', 'Online', 'Scoreboard', 'Exit']
#game list menu
games = ["Snake", "Tic tac toe", "Tetris", "Pong", "RPS", "Return Home"]


#the main fonction where everithing happens
def main(stdscr):
    #no cursor
    curses.curs_set(0)

    #set color pair
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    
    #current row main menu
    current_row = 0
    #current row sub menu
    submenu_row = 0
    #current row exit menu
    exit_row = 1 
    
    menu(stdscr, current_row, m_menu, "Game Palace:")
    while True:
        
        key = stdscr.getch()
        
        stdscr.erase()
        
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(m_menu)-1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            #play
            if current_row == 0:
                rnd_game = random.choice(games[0:5])
                if rnd_game == 'Snake':
                    snake.snake_start()
                elif rnd_game == 'Tic tac toe':
                    xo.xo_start()
                elif rnd_game == 'RPS':
                    rps.rps_start()
                else:
                    stdscr.addstr(0, 0, rnd_game)
                    stdscr.refresh()
                    stdscr.getch()
            #games list   
            elif current_row == 1:
                while True:
                    stdscr.erase()
                    menu(stdscr, submenu_row, games, "Games list:")
                    key = stdscr.getch()
                    if key == curses.KEY_UP and submenu_row > 0:
                        submenu_row -= 1
                    elif key == curses.KEY_DOWN and submenu_row < len(games)-1:
                        submenu_row += 1
                    elif key == curses.KEY_ENTER or key in [10, 13]:
                        if submenu_row == 0:
                            snake.snake_start()
                        elif submenu_row == 1:
                            xo.xo_start()
                        elif submenu_row == 2:
                            snow.Snow()
                        elif submenu_row == 3:
                            snow.Snow()
                        elif submenu_row == 4:
                            rps.rps_start()
                        elif submenu_row == 5:
                            submenu_row = 0
                            break
            #multiplayer mode
            elif current_row == 2:
                asciiAnimation.animate('earth/earth.txt', "UNDER DEVELOPMENT")
            #scoreboard
            elif current_row == 3:
                leaderboard.write_score()
            #exit
            if current_row == 4:
                while True:
                    stdscr.erase()
                    quit_menu(stdscr, exit_row)
                    key = stdscr.getch()
                    if key == curses.KEY_LEFT and exit_row > 0:
                        exit_row -= 1
                    elif key == curses.KEY_RIGHT and exit_row < 1:
                        exit_row += 1
                    elif key == curses.KEY_ENTER or key in [10, 13]:
                        if exit_row == 0:
                            sys.exit()
                        else:
                            break
                        
        menu(stdscr, current_row, m_menu, "Game Palace:")
        
        stdscr.refresh()

def run_app():
    curses.wrapper(main)