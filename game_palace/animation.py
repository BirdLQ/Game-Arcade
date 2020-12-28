import curses, time
import main_menu


#intro text
intro_text = ["      ___           ___           ___           ___                    ___         ___                         ___           ___           ___     ",
              "     /\__\         /\  \         /\  \         /\__\                  /\  \       /\  \                       /\  \         /\__\         /\__\    ",
              "    /:/ _/_       /::\  \       |::\  \       /:/ _/_                /::\  \     /::\  \                     /::\  \       /:/  /        /:/ _/_   ",
              "   /:/ /\  \     /:/\:\  \      |:|:\  \     /:/ /\__\              /:/\:\__\   /:/\:\  \                   /:/\:\  \     /:/  /        /:/ /\__\  ",
              "  /:/ /::\  \   /:/ /::\  \   __|:|\:\  \   /:/ /:/ _/_            /:/ /:/  /  /:/ /::\  \   ___     ___   /:/ /::\  \   /:/  /  ___   /:/ /:/ _/_ ",
              " /:/__\/\:\__\ /:/_/:/\:\__\ /::::|_\:\__\ /:/_/:/ /\__\          /:/_/:/  /  /:/_/:/\:\__\ /\  \   /\__\ /:/_/:/\:\__\ /:/__/  /\__\ /:/_/:/ /\__\ ",                  
              " \:\  \ /:/  / \:\/:/  \/__/ \:\~~\  \/__/ \:\/:/ /:/  /          \:\/:/  /   \:\/:/  \/__/ \:\  \ /:/  / \:\/:/  \/__/ \:\  \ /:/  / \:\/:/ /:/  /",
              "  \:\  /:/  /   \::/__/       \:\  \        \::/_/:/  /            \::/__/     \::/__/       \:\  /:/  /   \::/__/       \:\  /:/  /   \::/_/:/  / ",
              "   \:\/:/  /     \:\  \        \:\  \        \:\/:/  /              \:\  \      \:\  \        \:\/:/  /     \:\  \        \:\/:/  /     \:\/:/  /  ",
              "    \::/  /       \:\__\        \:\__\        \::/  /                \:\__\      \:\__\        \::/  /       \:\__\        \::/  /       \::/  /   ",
              "     \/__/         \/__/         \/__/         \/__/                  \/__/       \/__/         \/__/         \/__/         \/__/         \/__/    "]

#function to show and animate game name
def intro_anim(stdscr):
    
    curses.curs_set(0)
    stdscr.nodelay(1)
    
    #colors
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_CYAN, curses.COLOR_BLACK)
    
    height, width = stdscr.getmaxyx()
    
    x = width//2 - len(intro_text[0])//2
    y = height//2 - (len(intro_text)+5)//2
    
    color_number = 3
    
    notice = 'PRESS ENTER TO CONTINUE'
    
    movement = 0
    
    while True:
        stdscr.border(0)
        stdscr.addstr(height//2+len(intro_text)-5, width//2-len(notice)//2, notice, curses.A_STANDOUT)
        for i in range(len(intro_text)):
            for j in range(len(intro_text[i])):
                if j >=57:
                    if (j-8)%14==0:
                        color_number +=1
                else:
                    if j%14==0:
                        color_number +=1
                if color_number > 8:
                    color_number = 3
                stdscr.addstr(y + i + movement, x+j, intro_text[i][j], curses.color_pair(color_number))     
            color_number=3
            
        movement+=1
        
        if movement == 1:
            movement = movement*(-1)
        elif -1 == movement:
            movement = abs(movement)
        
        key = stdscr.getch()
        
        if key == curses.KEY_ENTER or key in [10, 13]:
            stdscr.nodelay(0)
            break
        time.sleep(0.5)
        stdscr.erase()
        
    main_menu.run_app()
    
def main_anim():
    curses.wrapper(intro_anim)