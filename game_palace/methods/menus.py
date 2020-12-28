import curses

def menu(stdscr, actual_row, items_list, title):
    stdscr.clear()
    
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    
    height, width = stdscr.getmaxyx()
    
    x = width//2 - len(title)//2
    y = height//2 - len(items_list)//2
    
    stdscr.addstr(y-2, x, title, curses.A_STANDOUT)
    
    for index, row in enumerate(items_list):
        
        x = width//2 - len(title)//2+1
        y = height//2 - len(items_list)//2 + index
        
        if index == actual_row:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x-1, '>'+row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
            
        stdscr.refresh()

def quit_menu(stdscr, actual_row):
    stdscr.clear()
    
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    
    height, width = stdscr.getmaxyx()
    
    exit_title = "Are you sure ?"
    
    x = width//2 - len(exit_title)//2
    y = height//2 - 2
    
    stdscr.addstr(y-2, x, exit_title, curses.A_STANDOUT)
    
    picker = '>'
    
    for index, row in enumerate(['Yes', 'No']):
            
        x = width//2 - len(row)//2 + index-3
        y = height//2 - 2
        
        if index == actual_row:
            stdscr.attron(curses.color_pair(1))
            if index == 1:
                stdscr.addstr(y, x+4, picker+row)
            else:
                stdscr.addstr(y, x-1, picker+row)
            stdscr.attroff(curses.color_pair(1))
        else:
            if index == 1:
                stdscr.addstr(y, x+5, row)
            else:
                stdscr.addstr(y, x, row)
            
        stdscr.refresh()