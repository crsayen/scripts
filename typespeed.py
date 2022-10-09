#!/usr/local/bin/python3.10
from pynput.keyboard import Key, Listener
from time import time
import sys
import re


def purple(s): return f"\033[95m{s}\033[0m"


def green(s): return f'\033[92m{s}\033[0m'


def bold(s): return f'\033[1m{s}\033[0m'


print(f"""
{purple("this program calculates how quickly you type arbitrary text.")}

⏵ the timer starts when you start typing 🖐️
⏵ the test ends when you press the enter key {green("↩")}
⏵ the timer ends when the key before enter is pressed

{bold(green("start typing to begin..."))}
    """)


def pad_center_justified(content, field_width):
    content_width = len(str(content))
    needs_offset = field_width % 2 != content_width % 2
    pad = (field_width - content_width) // 2
    return f"{' ' * (pad + needs_offset)}{content}{' ' * pad}"


def format_elapsed_time(seconds, field_width):
    integral_width = len(str(round(seconds)))
    is_room_for_decimal = field_width > integral_width + len(".99 s ")
    rounded = round(seconds, 2 if is_room_for_decimal else 0)
    return pad_center_justified(f"{rounded} s", field_width)


def format_number_of_words(words, field_width):
    return pad_center_justified(words, field_width)


def format_words_per_minute(seconds, words, field_width):
    wpm = round(words / (seconds / 60))
    return pad_center_justified(f"{wpm} WPM", field_width)


def on_match(pattern, text, fn):
    return fn(text) if re.fullmatch(pattern, text) else text


def colorize(s):
    chunks = s.split(' ')
    if re.fullmatch(r'[a-zA-Z0-9 \\.\n]+', s):
        return ' '.join([on_match(r'[\d\.]+', t, purple) for t in chunks])
    return ' '.join([on_match(r'[a-zA-Z ]+', t, green) for t in chunks])


template = """
╭─────────────────┬────────────╮
│ elapsed time    │_{}_________│
├─────────────────┼────────────┤
│ number of words │_{}_________│
╰─────────────────┴────────────╯
╭──────────────────────────────╮
│                              │
│______________{}______________│
│                              │
╰──────────────────────────────╯
"""


def build_table(start, end, text):
    number_of_words = len(text.strip().split(' '))
    seconds_elapsed = end - start
    populated_template = template.format(
        format_elapsed_time(seconds_elapsed, 12),
        format_number_of_words(number_of_words, 12),
        format_words_per_minute(seconds_elapsed, number_of_words, 30)
    )

    return "".join([colorize(s) for s in populated_template.split('_')])


if __name__ == '__main__':
    class State:
        TEXT = ''
        START_TIME = 0
        END_TIME = 0

    def on_release(key):
        if key != Key.enter:
            State.END_TIME = time()
        else:
            print(build_table(
                State.START_TIME,
                State.END_TIME,
                State.TEXT
            ))
            sys.stdin.readline()
            return False

    def on_press(key):
        if State.START_TIME == 0:
            State.START_TIME = time()
        try:
            State.TEXT += key.char
        except Exception:
            if key in [Key.space, Key.tab]:
                State.TEXT += ' '
            elif key == Key.backspace:
                State.TEXT = State.TEXT[:-1]

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
