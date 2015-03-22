import twitch
import config
import select
import sys
from datetime import datetime
import logging
logging.basicConfig( filename='input.log', level = logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y/%m/%d %I:%M:%S')
class MyInput:
    t = None
    inputbuffer = None
    
    def __init__(self):
        t = twitch.Twitch()
        t.set(config.username, config.key, config.room)
        t.connect()
        t.join()
        self.t = t
        self.inputbuffer = [sys.stdin, t.s]

    def getdata(self):
        while True:
            inputready, outputready, exceptready = select.select(self.inputbuffer, [], [], 0)
            for x in inputready:
                timestamp = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S");
                if x == sys.stdin:
                    uinput = input()
                    re = [{"From": "stdin", "msg": uinput, "time": timestamp}]
                    logging.info("stdin:" + uinput)
                    yield re
                elif x == self.t.s:
                    re = self.t.new_msg()
                    for y in re:
                        logging.info(y["From"] + ":" + y["msg"])
                    if re: 
                        yield re
            yield False


if __name__ == "__main__":
    t = MyInput()
    input_generator = t.getdata()
    while True:
        MSG = input_generator.__next__()
        From = MSG["From"]
        msg = MSG["msg"].lower()
        timestamp = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S");
        if From == "stdin":
            if msg == "exit":
                sys.exit()
        else:
            print(msg)
