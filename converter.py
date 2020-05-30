import struct


class Converter:
    def __init__(self, data):
        self.data = data
        self.header = self.parse_header()
        int_flags = bin(self.header[1])
        self.flags = '0' * (16 - len(int_flags) + 2) + str(int_flags)[2:]
        self.is_answer = self.flags[0]
        self.name, self.q_type, position = self.parse_question()
        self.info = None
        if self.is_answer:
            self.info = self.parse_body(position)

    def parse_header(self):
        header = struct.unpack("!6H", self.data[0:12])
        return header

    def parse_question(self):
        name, end = self.parse_name2(12)
        q_type, q_class = struct.unpack("!HH", self.data[end: end + 4])
        print("QUESTION", name, q_type, q_class, end + 4)
        return name, q_type, end + 4

    def parse_name2(self, start):
        name_list = []
        position = start
        # print("NAME_START", start)
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
                        flag = True
                    break
                position += 1
                name_list.append(self.data[position: position + length])
                position += length
        name = ".".join([i.decode('ascii') for i in name_list])
        return name, end

    def parse_body(self, start):
        print("ANSWERS")
        answer_list, end1 = self.parse_rr(start, 3)
        print("AUTHORITY")
        authority_list, end2 = self.parse_rr(end1, 4)
        print("ADDITIONAL")
        additional_list, end3 = self.parse_rr(end2, 5)
        return answer_list + authority_list + additional_list

    def parse_rr(self, start, number):
        offset = start
        rr_list = []
        result = []
        for i in range(self.header[number]):
            name, end = self.parse_name2(offset)
            # print(name, end)
            offset = end
            r_type, r_class, r_ttl, rd_length = struct.unpack("!2HIH", self.data[offset: offset + 10])
            print(
                "\tname {0}, type {1}, class {2}, ttl {3}, rd_len {4}".format(name, r_type, r_class, r_ttl, rd_length))

            offset += 10
            if r_type == 1:
                ip = struct.unpack("!4B", self.data[offset: offset + 4])
                print("\t\tIP", ip)
                offset += 4
                rr_list.append((name, r_type, r_ttl, ip))
            elif r_type == 2:
                dns_server_name, dns_name_end = self.parse_name2(offset)
                print("\t\tDNS_NAME", dns_server_name, dns_name_end)
                offset = dns_name_end
                rr_list.append((name, r_type, r_ttl, dns_server_name))
            else:
                offset += rd_length

        return rr_list, offset
