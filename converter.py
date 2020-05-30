import struct


class Converter:
    def __init__(self, data):
        self.data = data
        self.header = self.parse_header()
        int_flags = bin(self.header[1])
        self.flags = '0' * (16 - len(int_flags) + 2) + str(int_flags)[2:]
        self.is_answer = self.flags[0]
        self.parse_question()

    def parse_header(self):
        header = struct.unpack("!6H", self.data[0:12])
        return header

    def parse_question(self):
        tail = self.data[12:]
        name_list = []
        position = 0
        while tail[position] != 0:
            length = tail[position]
            name_list.append(tail[position + 1:position + length + 1])
            position += length + 1
            # print(position)
        # print(name_list)
        position += 1
        q_name = ".".join([i.decode('ascii') for i in name_list])
        q_type, q_class = struct.unpack("!HH", tail[position: position + 4])
        print(q_name, q_type, q_class)

    def parse_name(self, start):
        tail = self.data[start:]
        name_list = []
        position = 0
        while tail[position] != 0:
            length = tail[position]
            name_list.append(tail[position + 1:position + length + 1])
            position += length + 1
        position += 1
        name = ".".join([i.decode('ascii') for i in name_list])
        return name
