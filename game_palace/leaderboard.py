import csv, curses, locale, os, pyAesCrypt
from curses import textpad

import main_menu

#set encodage to utf-8
locale.setlocale(locale.LC_ALL, '')


def txtpnl(stdscr, wl=12):
    global s
    stdscr.clear()
    curses.init_pair(9, curses.COLOR_RED, curses.COLOR_BLACK)
    
    height, width = stdscr.getmaxyx()
    xl = width//2 - wl//2-1
    y = height//2
    
    title = "Enter your name :"
    warning = "INVALID ENTRY !" 
    
    stdscr.addstr(y-1, width//2 - len(title)//2, title, curses.A_STANDOUT)
    
    wl += xl + 2
    s = ''
    textpad.rectangle(stdscr, y, xl, y + 2, wl)
    stdscr.addstr(y + 1, xl + 1, '')
    cp = 0
    while True:
        textpad.rectangle(stdscr, y, xl, y + 2, wl)
        stdscr.addstr(y + 1, xl + 1 + cp, '')
        k = stdscr.getch()
        if k == curses.KEY_ENTER or k in [10, 13]:
            if s.isalnum():
                break
            else:
                stdscr.attron(curses.color_pair(9))
                stdscr.addstr(y+3, width//2 - len(warning)//2, warning, curses.A_BOLD)
                stdscr.attroff(curses.color_pair(9))
        elif k == curses.KEY_UP or k == curses.KEY_DOWN:
            pass
        elif k == curses.KEY_BACKSPACE or k == 8:
            if cp > 0: cp -= 1
            stdscr.addstr(y + 1, xl + 1, " " * len(s))
            s = s[:cp]+s[cp+1:]
            stdscr.addstr(y + 1, xl + 1 + cp, s[cp:])
            stdscr.addstr(y + 1, xl + 1, s[:cp])

        elif k == curses.KEY_LEFT or k == 27:
            if not cp:
                pass
            else:
                cp -= 1
                
        elif k == curses.KEY_RIGHT or k == 26:
            if cp == len(s):
                pass
            else:
                cp += 1
                stdscr.addstr(y + 1, xl + 1 + cp, s[cp:])
                stdscr.addstr(y + 1, xl + 1, s[:cp])
                
        elif k in [curses.KEY_DC, 127]:
            stdscr.addstr(y + 1, xl + 1 + cp, s[cp + 1:] + " ")
            stdscr.addstr(y + 1, xl + 1, s[:cp])
            s = s[:cp] + s[cp + 1:]
        else:
            if len(s) < wl - xl - 2:
                if cp == len(s):
                    s += str(chr(k))
                    stdscr.addstr(y + 1, xl + 1, s)
                else:
                    s = s[:cp] + str(chr(k)) + s[cp:]
                    stdscr.addstr(y + 1, xl + 1 + len(s[:cp + 1]), s[cp + 1:])
                    stdscr.addstr(y + 1, xl + 1, s[:cp + 1])
                    
                cp += 1
    return s


def text_entry():    
    curses.wrapper(txtpnl)
    return s


"""
TO ADD: arrange csv each time its opened
"""
#encryption/decryption buffer size - 64K
bufferSize = 64 * 1024
password = "Fdv54wH8L2hKSfz2"

def save_score(name="", snake_score = 0, ttt_score = 0, tetris_score = 0, pong_score = 0, rps_score = 0):
    #decrypt
    pyAesCrypt.decryptFile("data/tableader.csv.aes", "data/tableader.csv", password, bufferSize)
    
    #open file add append data
    with open("data/tableader.csv", "a", newline='') as file:
        fields= ['Username', 'Snake', 'Tic tac toe', 'Tetris', 'Pong', 'RPS']
        writer=csv.DictWriter(file, fieldnames=fields)
        writer.writerow({'Username': name, 'Snake': snake_score,
                              'Tic tac toe': ttt_score, 'Tetris': tetris_score,
                              'Pong': pong_score, 'RPS': rps_score})
        
    #encrypt       
    pyAesCrypt.encryptFile("data/tableader.csv", "data/tableader.csv.aes", password, bufferSize)
    
    #remove not encrypted file
    os.remove("data/tableader.csv")

def scoreboard(stdscr):
    #decrypt
    pyAesCrypt.decryptFile("data/tableader.csv.aes", "data/tableader.csv", password, bufferSize)
    
    #read file
    with open ("data/tableader.csv", "r") as file:
        sortlist=[]
        reader=csv.reader(file)
        for i in reader: 
            sortlist.append(i)
            
    #encrypt       
    pyAesCrypt.encryptFile("data/tableader.csv", "data/tableader.csv.aes", password, bufferSize)
    
    #remove not encrypted file
    os.remove("data/tableader.csv")
    
    #remove all blank names
    sortlist = [sortlist[i] for i in range(len(sortlist)) if sortlist[i][0]!='']
    
    #append names in names
    names = [sortlist[i][:1] for i in range(len(sortlist))]
    
    #append scores in scores
    scores = [sortlist[i][1:] for i in range(len(sortlist))]
    
    #convert list to int
    for i in range(len(scores)):
        scores[i] = list(map(int, scores[i]))
    
    #sum scores
    scores = [sum(scores[i]) for i in range(len(scores))]
    
    #append [name - total score] of every player
    result=[]
    for i in range(len(names)):
        result.append([*names[i], scores[i]])
    
    """
    check if name is not duplicate
    if there is duplicate add score
    """
    dummy = {}
    for name,score in result:
        total = dummy.get(name,0) + score
        dummy[name] = total
            
    result.clear()
    
    #convert dict (dummy) to list
    for key, value in dummy.items():
        temp = [key,value]
        result.append(temp)
    
    #sort list by decreasing score 
    def myFunc(e):
      return e[1]

    result.sort(reverse=True, key=myFunc)
    
    stdscr.clear()
    curses.curs_set(0)
    
    height, width = stdscr.getmaxyx()
    x = width//2 - 13
    y = height//2 - 8
    
    h1 = 'TOP SCORES:'
    
    stdscr.addstr(height//2 - 10, width//2 - len(h1)//2, h1, curses.A_STANDOUT)
    
    for i in range(10):
        try:
            tps = str(result[i][1])
            tab = 12-len(result[i][0])
            stdscr.addstr(y+i, x + tab, result[i][0], curses.A_BOLD)
            stdscr.addstr(y+i, x + 16, tps, curses.A_BOLD)
        except:
            stdscr.addstr(y+i, x, '------------    ------------')
        stdscr.refresh()
            
    while True:
        key = stdscr.getch()
        if key == curses.KEY_EXIT or key == 27:
            main_menu.run_app()
            
            
def write_score():        
    curses.wrapper(scoreboard)