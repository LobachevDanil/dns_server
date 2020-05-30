import socket

from cache import Cache
from converter import Converter


class Server:
    def __init__(self):
        self.cache = Cache()

    def start(self):
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.bind(('192.168.1.153', 53))
                data, addr = sock.recvfrom(1024)
                print(addr)
                self.print_packet(data)
                c = Converter(data)
                print(c.header)
                print(c.flags)
                print(c.is_answer)

    def print_packet(self, data):
        for i in range(len(data)):
            print("{0:4}".format(str(hex(data[i]))), end=" ")
            if i % 16 == 0:
                print()
        print()


def main():
    Server().start()


if __name__ == '__main__':
    main()
