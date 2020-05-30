import pickle
import os.path
import time


class Cache:
    def __init__(self):
        self.filename = 'cache'
        self.data = self.load()

    def save(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self.data, f)
            print("Save cache")

    def load(self):
        if not os.path.exists(self.filename):
            return dict()
        with open(self.filename, 'rb') as f:
            data = pickle.load(f)
            need_delete = []
            for k, v in data.items():
                if v[1] + v[2] <= time.time():
                    need_delete.append(k)
            for k in need_delete:
                data.pop(k)
            print("Load cache", data)
        return data

    def try_get_item(self, key):
        if key in self.data:
            value = self.data[key]
            if value[1] + value[2] >= time.time():
                print("Give", key, "->", value[0])
                return True, value
        return False, None

    def put(self, name, type, ttl, item):
        self.data[(name, type)] = (item, time.time(), ttl)
        print("Add key", (name, type))
