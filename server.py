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
                self.print_packet(data)
                c = Converter(data)
                is_contain, value = self.cache.try_get_item((c.name, c.q_type))
                if is_contain:
                    print("magic", value)
                else:
                    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as dns:
                        dns.bind(("192.168.1.153", 55555))
                        dns.sendto(data, ("8.8.8.8", 53))
                        out = dns.recvfrom(1024)[0]

                    sock.sendto(out, addr)
                    c2 = Converter(out)
                    self.cache.put('d', 'NS', 'test', 10000)

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
