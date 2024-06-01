import curses
from curses import wrapper
import time
import random

def display_welcome_message(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the Typing Test!")
    stdscr.addstr("\nPress any Enter to begin....!!")
    stdscr.refresh()
    stdscr.getkey()

def render_text(stdscr, target_string, current_string, wpm_count=0):
    stdscr.addstr(target_string)
    stdscr.addstr(1, 0, f"WPM: {wpm_count}")
    for index, char in enumerate(current_string):
        correct_char = target_string[index]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)
        stdscr.addstr(0, index, char, color)

def fetch_random_text():
    with open("text.txt", "r") as file:
        lines = file.readlines()
        return random.choice(lines).strip()

def start_typing_test(stdscr):
    target_text = fetch_random_text()
    current_text = []
    wpm_count = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm_count = round((len(current_text) / (time_elapsed / 60)) / 5)

        stdscr.clear()
        render_text(stdscr, target_text, current_text, wpm_count)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:
            break

        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)

def main_function(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    display_welcome_message(stdscr)
    while True:
        start_typing_test(stdscr)
        stdscr.addstr(2, 0, "You completed the text! Press any key to continue...")
        key = stdscr.getkey()

        if ord(key) == 27:
            break

wrapper(main_function)