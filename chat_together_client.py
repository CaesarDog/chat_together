from socket import *
import os, sys

ADDR = ("127.0.0.1", 8888)


def send_msg(s, name):
    while True:
        try:
            text = input(">>")
        except KeyboardInterrupt:
            text = "quit"
        if text == "quit":
            msg = "Q "+ name
            s.sendto(msg.encode(),ADDR)
            sys.exit("退出聊天室")

        msg = "C %s %s"%(name,text)
        s.sendto(msg.encode(), ADDR)

def recv_msg(s):
    while True:
        data,addr = s.recvfrom(1024)
        if data.decode() == "EXIT":
            sys.exit()
        # name = data.decode().split(" ")[0]
        # msg = data.decode().split(" ")[1]
        print(data.decode())

def main():
    sockfd = socket(AF_INET, SOCK_DGRAM)
    # sockfd.bind(("172.20.10.4",8888))
    while True:
        name = input("请输入姓名:")
        msg = "L " + name
        sockfd.sendto(msg.encode(), ADDR)
        # 等待回应
        data, addr = sockfd.recvfrom(1024)
        if data.decode() == "success":
            print("你已进入聊天室")
            break
        else:
            print(data.decode())
    pid = os.fork()
    if pid < 0:
        sys.exit("Error")
    elif pid == 0:
        send_msg(sockfd, name)
    else:
        recv_msg(sockfd)
        # msg = "C "+input(">>")
        # data,addr = sockfd.recvfrom(1024)


if __name__ == '__main__':
    main()
