import time, curses

def progressBar(stdscr, iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    curses.curs_set(0)
    
    height, width = stdscr.getmaxyx()
    
    x = width//2 - 76//2
    
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    total = len(iterable)
    # Progress Bar Printing Function
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        stdscr.addstr(height//2, x, f'{prefix} |{bar}| {percent}% {suffix}')
        stdscr.refresh()
    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    
# A List of Items
items = list(range(0, 57))

def main(stdscr):
    for item in progressBar(stdscr, items, prefix = 'Loading...', suffix = '', length = 50):
        time.sleep(0.01)

def load():
    curses.wrapper(main)