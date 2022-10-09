#!/usr/local/bin/python3.10
from pynput.keyboard import Key, Listener
from time import time
import sys

class Color:
    PURPLE = '\033[95m'
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    DIM = '\033[22m'
    END = '\033[0m'

text = ''
start = 0
end = 0

def on_press(key):
    global text
    global start

    if start == 0: start = time()

    try: 
        text += key.char
    except:
        if key in  [Key.space]:
            text += ' '


def on_release(key):
    global end
    if key != Key.enter:
        end = time()
    else:
        print()

        
        elr_field_size = 8
        el = end - start
        el_integral_text_size = len(str(round(el)))
        elr = round(el, max(0, elr_field_size - (el_integral_text_size + 1)))
        elr_text_len = len(str(elr))
        elr_fill = ' ' * (elr_field_size - elr_text_len)
                 
        nwords = len(text.strip().split(' '))
        nwords_text_len = len(str(nwords))
        nwords_field_size = 8
        nwords_fill = ' ' * (nwords_field_size - nwords_text_len)
        
        print(f'{Color.YELLOW}┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓{Color.END}')
        print(f'{Color.YELLOW}┃{Color.END} elapsed time    {Color.YELLOW}┃{Color.END} {elr} seconds {elr_fill}{Color.YELLOW}┃{Color.END}')
        print(f'{Color.YELLOW}┣━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━┫{Color.END}')        
        print(f'{Color.YELLOW}┃{Color.END} number of words {Color.YELLOW}┃{Color.END} {nwords}{nwords_fill}         {Color.YELLOW}┃{Color.END}')
        print(f'{Color.YELLOW}┗━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━┛{Color.END}')

        nmins = elr / 60
        print(f'\n{Color.BOLD}{Color.PURPLE}{round(nwords / nmins)}{Color.END} WPM{Color.END}')
        
        sys.stdin.readline()

        return False
    
print("\nthis program calculates how quickly you type arbitrary text.\n")
print(f"{Color.BOLD}⏵ the timer starts when you start typing 🖐️{Color.END}")    
print(f"{Color.BOLD}⏵ the test ends when you press the enter key {Color.PURPLE}↩{Color.END}")    
print(f"{Color.BOLD}⏵ the time that the last key before the enter key is pressed is the ending time{Color.END}")
print(f"  {Color.YELLOW}in other words, waiting a while before pressing enter will not affect your score{Color.END}")
print("\nstart typing to begin...\n")
    
with Listener(
    on_press=on_press,
    on_release=on_release) as listener:
    listener.join()
    