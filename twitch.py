import socket
import sys
import re
from datetime import datetime

class Twitch:
    user = "";
    oauth = "";
    room = "";
    s = None;

    def detail(self):
        print(self.user)
        print(self.oauth)
        print(self.room)

    def set(self, user, oauth, room):
        self.user = user
        self.oauth = oauth
        self.room = room

    def connect(self):
        print("Connecting to twitch")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        connect_host = "irc.twitch.tv"
        connect_port = 6667
        try:
            s.connect((connect_host, connect_port))
        except:
            print("Fail at create connection to twitch~")
            sys.exit()
        print("Sending Detail...")
        s.sendall( (("USER {}\r\n").format(self.user)).encode() )
        s.sendall( (("PASS {}\r\n").format(self.oauth)).encode() )
        s.sendall( (("NICK {}\r\n").format(self.user)).encode() )

        if not self.login_status(s.recv(1024)):
            print("Failed at Login~")
            sys.exit()
        else:
            self.s = s
            print("Connected.")
        

    def login_status(self, data):
        if data == "b':tmi.twitch.tv NOTICE * :Login unsuccessful\r\n'": return False
        else: return True

    def join(self):
        self.s.send( (("JOIN #{}\r\n").format(self.room)).encode() )
        message = self.s.recv(1024)
        self.s.settimeout(0.5);

    def receive(self):
        message = None
        try:
            message = self.s.recv(1024)
            return message.decode()
        except:
            return False

    def parse(self, data):
        timestamp = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        try:
            result = re.search(":(\w+)![\w+@_+\.]+ PRIVMSG #(\w+) :(.*)", data)
            result = {"From": result.group(1), "msg": result.group(3), "time": timestamp}
            return result
        except:
            return False

    def new_msg(self):
        data = self.receive()
        if not data: return [];
        data = data.split('\r\n')
        re = []
        for msg in data:
            if msg == "PING :tmi.twitch.tv":
                self.s.sendall(('PONG :tmi.twitch.tv\r\n').encode())
            else:
                tmp = self.parse(msg)
                if tmp: re.append(tmp)
        return re
                

