import random
import socket
from _thread import *
import sys

server = "00.00.00.000"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1]), int(str[2]), int(str[3]), int(str[4]), int(str[5]), int(str[6])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])+ "," + str(tup[2])+ "," + str(tup[3])+ "," + str(tup[4])+ "," + str(tup[5])+ "," + str(tup[6])


p2PosX = 735
p2PosY = 770
isBeamShotPlayer = 0
BossBeamX = random.randint(0,1600)
BossHp = 75
PlayerHp = 1
currentPlayer = 0
bossBeamCooldown = 60


pos = [(p2PosX,p2PosY,isBeamShotPlayer,BossHp,PlayerHp,BossBeamX,currentPlayer),(p2PosX,p2PosY,isBeamShotPlayer,BossHp,PlayerHp,BossBeamX,currentPlayer)]
##
def threaded_client(conn, player):
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""
    while True:
        try:

            data = read_pos(conn.recv(4096).decode())
            pos[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]

                print("Received: ", data)
                replyL = list(reply)
                replyL[5] = BossBeamX
                replyL[6] = currentPlayer
                reply = tuple(replyL)
                print("Sending : ", reply)
            conn.sendall(str.encode(make_pos(reply)))
        except:
            break

    print("Lost connection")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1  