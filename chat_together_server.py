from socket import *
import os, sys

ADDR = ("0.0.0.0", 8888)
user = {}


def do_login(s, name, addr):
    if name in user:
        s.sendto("用户已存在".encode(), addr)
        return
    s.sendto(b"success", addr)
    # 通知其他人
    msg = "欢迎%s进入聊天室" % name
    user[name] = addr
    for i in user:
        s.sendto(msg.encode(), user[i])


def do_chat(s, name, text):
    for item in user:
        if item != name:
            s.sendto((name+":"+text).encode(), user[item])


def do_quit(s, name):
    msg = "%s退出了聊天室" % name
    for i in user:
        if i != name:
            s.sendto(msg.encode(), user[i])
        else:
            s.sendto(b"EXIT", user[i])
    del user[name]


def do_request(s):
    while True:
        data, addr = s.recvfrom(1024)
        msg = data.decode().split(" ")
        if msg[0] == "L":
            do_login(s, msg[1], addr)
        elif msg[0] == "C":
            text = " ".join(msg[2:])
            do_chat(s, msg[1], text)
        elif msg[0] == "Q":
            do_quit(s, msg[1])


# 创建网络连接
def main():
    sockfd = socket(AF_INET, SOCK_DGRAM)

    sockfd.bind(ADDR)
    do_request(sockfd)
    # pid = os.fork()
    # if pid < 0:
    #     print("Error")
    # elif pid == 0:
    #     sockfd.sendto(data)
    #
    # data,address = sockfd.recvfrom(1024)


if __name__ == "__main__":
    main()
