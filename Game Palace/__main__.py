import animation, loading
import threading

#check if os is win else raise error
import platform
if platform.system() != 'Windows':
    raise "OPERATING SYSTEM NOT SUPPORTED"

#check if screen is not too small
from win32api import GetSystemMetrics
width = GetSystemMetrics(0)
height = GetSystemMetrics(1)
if width <= 1300 or height <= 600:
    raise 'SCREEN TOO SMALL'

#no error raised if launched in terminal
'''
#set game full screen
import win32console
display = win32console.GetStdHandle(win32console.STD_OUTPUT_HANDLE)
display.SetConsoleDisplayMode(win32console.CONSOLE_FULLSCREEN_MODE, win32console.PyCOORDType(0,0))
'''
import keyboard
keyboard.press('f11')

def beg():
    loading.load()   
    
thread_l = threading.Thread(target = beg)
    
thread_l.start()
    
while True:
    if not thread_l.is_alive():
        #file starting
        animation.main_anim()
