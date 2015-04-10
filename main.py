from myinput import MyInput
from datetime import datetime
import time
import sys
import keypress
import operator
import logging
logging.basicConfig( filename='twitch.log', level = logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y/%m/%d %I:%M:%S')

basic_command = ["up", "down", "left", "right", "a", "b", "enter", "select", "l", "r"]
class IRC_WITH_GAME:
    Input = MyInput()
    Input_generator = Input.getdata()
    mode = 2
    wait_time = 3
    cmd = []
    last_exec_time_s = None
    command = []

    def __init__(self):
        self.last_exec_time_s = time.time()
        self.command = basic_command

    def run(self):
        while True:
            Data = self.Input_generator.__next__()
            if not Data:
                self.Mode()
                continue
            for MSG in Data:
                From = MSG["From"]
                if From == "stdin":
                    msg = MSG["msg"]
                    if msg == "exit":
                        sys.exit()
                    elif msg[:5] == "mode=":
                        self.mode = int(msg[5:])
                    elif msg[:5] == "time=":
                        self.wait_time = int(msg[5:])

                else:
                    self.cmd.append(MSG)
    def mode_0(self):
        tmp = [0, 0, 0, 0];
        for X in self.cmd:
            try: x = int(X["msg"])
            except: x = 0
            if x == 1 or x == 2 or x == 3:
                tmp[x] += 1
        new_mode = 0
        new_mode_max = 0
        for i in range(1, 4):
            if tmp[i] > new_mode_max:
                new_mode = i
                new_mode_max = tmp[i]
        max_num = 0
        for i in range(1, 4):
            if tmp[i] == new_mode_max:
                max_num += 1
        if max_num > 1:
            new_mode = 0
        self.mode = new_mode
        self.command = basic_command
        msg = "Mode: " + str(new_mode)
        logging.info(msg)
        print(msg)
        
        
    def mode_1(self):
        key = []
        for X in self.cmd:
            x = X["msg"]
            while len(x):
                flag = False
                for y in self.command:
                    if x[0:len(y)] == y:
                        key.append(y)
                        x = x[len(y):]
                        flag = True
                        break
                if not flag: x = x[1:]
        print(key)
        return key

    def mode_2(self):
        key = []
        tmp = [0 for i in range(len(self.command))]
        for X in self.cmd:
            x = X["msg"]
            while len(x):
                flag = False
                for i in range(len(self.command)):
                    if x[:len(self.command[i])] == command[i]:
                        flag = True
                        x = x[len(self.command[i]):]
                        tmp[i] += 1
                        break
                if not flag: cmd = cmd[1:]
        
        remain_cmd = []
        max_value = 0
        for i in range(len(self.command)):
            if tmp[i] == max_value:
                remain_cmd.append(self.command[i])
            elif tmp[i] > max_value:
                max_value = tmp[i]
                remain_cmd = [self.command[i]]
        self.command = remain_cmd
        if len(self.command) == 1:
            key = self.command
            self.command = basic_command
        return key

    def mode_3(self):
        print("3")


    def Mode(self):
        if self.last_exec_time_s + self.wait_time >= time.time(): return

        mode = self.mode
        key = []
        if mode == 0:
            self.mode_0()
        elif mode == 1:
            key = self.mode_1()
        elif mode == 2:
            key = self.mode_2()
        elif mode == 3:
            key = self.mode_3()

        for x in key:
            keypress.press(x, 250)
            logging.info("[keydown]: " + x)
        self.cmd[:] = []
        self.last_exec_time_s = time.time()

if __name__ == "__main__":
    game = IRC_WITH_GAME()
    game.run()
