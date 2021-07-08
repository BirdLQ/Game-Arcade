from os import listdir, chdir, curdir
from os.path import isfile, join, abspath

from time import sleep
from random import choice

import curses

#minAnimationTime = 35

def drawAnimation(stdscr, width, height, path, msg):
    '''
        Show animation
    '''
    stdscr.clear()
    curses.curs_set(0)

    # choose animation
    #availableAnimations = [f for f in listdir('animations/') if not isfile(join('animations/', f))]
    #animationChosen = choice(availableAnimations)
    animationChosen = 'data/animations/'+path
    
    # get animation data
    #with open('animations/'+animationChosen+'/'+animationChosen+'.txt','r') as fin:
    with open(animationChosen, 'r') as fin:
        animationData = fin.read().split('[FILEBREAK]')
    
    cond = True
    #animationTime = 0
    while cond:
        #stdscr.clear()
        stdscr.nodelay(1)
        for frame in animationData:
            key = stdscr.getch()
            if key == curses.KEY_EXIT or key == 27:
                stdscr.nodelay(0)
                cond = False
                break

            frameLines = frame.split("\n")
            # show animation 'frame'
            y=15
            animationX = (width//2) - (len(frameLines[0])//2)
            
            #stdscr.erase()
            for line in frameLines:
                stdscr.addstr(y,animationX-33,line)
                stdscr.addstr(30, animationX - len(msg)//2, msg, curses.A_STANDOUT)
                y+=1
                #for big animations
                #if y >= height:
                 #   break

            #animationTime += 1

            stdscr.refresh()
            sleep(0.015)
