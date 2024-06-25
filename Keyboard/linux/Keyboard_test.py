#!/usr/bin/env python3
import sys, select, termios, tty
import keyboard_control
import time
from threading import Thread

from plutocontrol import pluto 

settings = termios.tcgetattr(sys.stdin)

keep_running = True
my_pluto = pluto()
my_pluto.cam()
my_pluto.connect()

def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist: 
        key = sys.stdin.read(1)
        if (key == '\x1b'):
            key = sys.stdin.read(2)
        sys.stdin.flush()
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


keyboard={  #dictionary containing the key pressed abd value associated with it
                      '[A': 10,
                      '[D': 30,
                      '[C': 40,
                      'w':50,
                      's':60,
                      ' ': 70,
                      'r':80,
                      't':90,
                      'p':100,
                      '[B':110,
                      'n':120,
                      'q':130,
                      'e':140,
                      'a':150,
                      'd':160,
                      '+' : 15,
                      '1' : 25,
                      '2' : 30,
                      '3' : 35,
                      '4' : 45,
                      'l': 170}


def clean_exit():
    global keep_running
    keep_running = False
    try:
        print("Disarming...")
        my_pluto.disarm()
        time.sleep(2)
        print("Disconnecting...")
        my_pluto.disconnect()
    except Exception as e:
        print(f"Exception during cleanup: {e}")
    finally:
        print("Exiting...")
        exit()

def keyList():
    global keep_running
    while keep_running:
        key = getKey()
        if key == 'e':
            print("stopping")
            keep_running = False
            clean_exit()
        if key in keyboard.keys():
            msg = keyboard[key]
            keyboard_control.identify_key(msg,my_pluto)
        else:
            msg = "80"
            keyboard_control.identify_key(msg,my_pluto)


if __name__ == "__main__":
    # keep_running = True
    listener_thread = Thread(target=keyList)
    listener_thread.start()
    try:
        while keep_running:
            time.sleep(0.1)
    except KeyboardInterrupt:
        keep_running = False
        print("keyInterrupt")
        clean_exit()
    listener_thread.join()