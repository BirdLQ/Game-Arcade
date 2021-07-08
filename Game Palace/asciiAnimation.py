from time import sleep
import curses
from methods.rendering import drawAnimation
import main_menu

def animate(path, msg):
    stdscr = curses.initscr()
    curses.cbreak()
    stdscr.keypad(1)

    height,width = stdscr.getmaxyx()
    
    try:
        #while 1:
        stdscr.clear()
            
        drawAnimation(stdscr, width, height, path, msg)

        stdscr.refresh()
            #sleep(1)

    finally:
        curses.nocbreak()
        stdscr.keypad(0)
        curses.echo()
        curses.endwin()
    
    main_menu.run_app()