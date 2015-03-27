from myinput import MyInput
from datetime import datetime
import time
import sys
import keypress
import operator
class IRC_WITH_GAME:
    Input = MyInput()
    Input_generator = Input.getdata()
    mode = 0
    wait_time = 1
    cmd = []
    last_exec_time = None
    last_exec_time_s = None

    def __init__(self):
        self.last_exec_time = self.now()

    def run(self):
        while True:
            Data = self.Input_generator.__next__()
            if not Data:
                self.Mode()
                continue
            print(Data)
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

    def Mode(self):
        command = ["up", "down", "left", "right", "a", "b", "enter", "select", "l", "r"]
        mode = self.mode
        key = []
        if mode == 0:
            for x in self.cmd:
                key = key + (self.parse(x["msg"]))
        elif mode == 1:
            if self.last_exec_time_s + self.wait_time >= time.time(): return
            ele = []
            tmp = {}
            for x in self.cmd:
                ele = ele + (self.parse(x["msg"]))
            for x in command:
                tmp[x] = 0
            for x in ele:
                tmp[x] += 1
            max_cmd = max(tmp.items(), key=operator.itemgetter(1))[0]
            if tmp[max_cmd] > 0:
                key.append(max_cmd)
        elif mode == 2:
            if self.last_exec_time == self.now(): return

        for x in key:
            keypress.press(x, 250)
        self.cmd[:] = []
        self.last_exec_time = self.now()
        self.last_exec_time_s = time.time()
        if key:
            print(key)


    def now(self):
        return datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")

    def parse(self, data):
        data = data.lower()
        re = [];
        command = ["up", "down", "left", "right", "a", "b", "enter", "select", "l", "r"]
        while len(data):
            flag = 0
            for x in command:
                if data[0:len(x)] == x:
                    re.append(x)
                    data = data[len(x):]
                    flag = 1
                    break
            #if not flag: return []
            if not flag: data = data[1:]
        return re

if __name__ == "__main__":
    game = IRC_WITH_GAME()
    game.run()
