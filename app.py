import re
import socket
import time

PINBALL = re.compile("([\d,]*[\d]+) points \(x(\d+)\) on the (red|blue|gold|silver) pinball table",)

TABLES = ["red", "blue", "gold", "silver"]

failed_auth_attempts = 0

def connect():
    s.connect(("irc.chat.twitch.tv", 6667))
    s.send(b"NICK justinfan123\n")
    s.send(b"JOIN #twitchplayspokemon\n")
s = socket.socket()
connect()

while 1:
    try:
        data = s.recv(2048).decode("utf-8").split("\r\n")[:-1]
    except ConnectionResetError:
        connect()
        time.sleep((failed_auth_attempts - 1) ** 2 * bool(failed_auth_attempts))
        continue
    for i in data:
        if PINBALL.search(i) is not None and i.startswith(":tpp"):
            x = PINBALL.split(i)
            table = TABLES.index(x[3])
            score = int(x[1].replace(",", "")) // 50
            data = ((score << 2) + table)
            data = data.to_bytes(4, "big")
            print(data, end="")
