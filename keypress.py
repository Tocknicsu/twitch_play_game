import subprocess
keymp = {
        "up": "Up",
        "down": "Down",
        "left": "Left",
        "right": "Right",
        "a": "z",
        "b": "x",
        #"l": "a",
        #"r": "s",
        "select": "q",
        "enter": "w",
        "u": "Up",
        "d": "Down",
        "l": "Left",
        "r": "Right"
        }


def press(key, delay):
    subprocess.call('xdotool search --onlyvisible --name VBA-M key --delay %d %s' % (delay, keymp[key]), shell=True)
