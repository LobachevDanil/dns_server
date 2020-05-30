import socket

from cache import Cache
from converter import Converter


class Server:
    def __init__(self):
        self.cache = Cache()

    def start(self):
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                    sock.bind(('192.168.1.153', 53))
                    data, addr = sock.recvfrom(1024)
                    parse_request = Converter(data)
                    is_contain, value = self.cache.try_get_item((parse_request.name, parse_request.q_type))
                    if is_contain:
                        p = parse_request.make_answer(value[2], value[0])
                        sock.sendto(p, addr)
                    else:
                        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as dns:
                            dns.bind(("192.168.1.153", 55555))
                            dns.sendto(data, ("ns1.e1.ru", 53))
                            out = dns.recvfrom(1024)[0]

                        sock.sendto(out, addr)
                        parse_answer = Converter(out)
                        for info in parse_answer.info:
                            self.cache.put(*info)
                print("-" * 30)
            except Exception as e:
                print("Was exception")
                print(e)
                raise
            else:
                self.stop()

    def stop(self):
        self.cache.save()

    def print_packet(self, data):
        i = 1
        for b in data:
            print("{0:4}".format(str(hex(b))), end=" ")
            if i % 16 == 0:
                print()
            i += 1
        print()


def main():
    Server().start()


if __name__ == '__main__':
    main()
