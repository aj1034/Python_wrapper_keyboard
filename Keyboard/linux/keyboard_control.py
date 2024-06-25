import sys, os, select, termios, tty
import subprocess

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


# from plutocontrol import pluto   # Importing the Pluto module for interfacing with the Pluto drone
# my_pluto = pluto()

settings = termios.tcgetattr(sys.stdin)

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
count = 0



def identify_key(key,my_pluto):
    if key == 70:
        if(my_pluto.rcAUX4 == 1500):
            my_pluto.disarm()
        else:
            my_pluto.arm()
    elif key == 10:
        my_pluto.forward()
    elif key == 30:
        my_pluto.left()
    elif key == 40:
        my_pluto.right()
    elif key == 80:
        my_pluto.reset()
    elif key == 50:
        my_pluto.increase_height()
    elif key == 60:
        my_pluto.decrease_height()
    elif key == 110:
        my_pluto.backward()
    elif key == 130:
        my_pluto.take_off()
    elif key == 140:
        my_pluto.land()
    elif key == 150:
        my_pluto.left_yaw()
    elif key == 160:
        my_pluto.right_yaw()
    # elif key == 170:
        # subprocess.run(["python3", "/home/atharva/drona/qr_landing.py"])
    
 
        