import struct


class Converter:
    def __init__(self, data):
        self.data = data
        self.header = self.parse_header()
        int_flags = bin(self.header[1])
        self.flags = '0' * (16 - len(int_flags) + 2) + str(int_flags)[2:]
        self.is_answer = self.flags[0]
        self.name, self.q_type, position = self.parse_question()

    def parse_header(self):
        header = struct.unpack("!6H", self.data[0:12])
        return header

    def parse_question(self):
        name, end = self.parse_name2(12)
        q_type, q_class = struct.unpack("!HH", self.data[end: end + 4])
        return name, q_type, end + 4

    def parse_name2(self, start):
        name_list = []
        position = start
        end = start
        flag = False
        while True:
            if self.data[position] > 63:
                if not flag:
                    end = position + 2
                    flag = True
                position = ((self.data[position] - 192) << 8) + self.data[position + 1]
                continue
            else:
                length = self.data[position]
                if length == 0:
                    if not flag:
                        end = position + 1
                    break
                position += 1
                name_list.append(self.data[position: position + length])
                position += length
        name = ".".join([i.decode('ascii') for i in name_list])
        print(name_list)
        return name, end
