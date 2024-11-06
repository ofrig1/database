from SerializeDatabase import SerializeDatabase
import threading
import multiprocessing


class SyncDatabase(SerializeDatabase):
    def __init__(self, mode='threads'):
        super().__init__()
        self.mode = mode
        self.max_readers = 10
        self.read_count = 0
        self.read_array = [0]*10
        # 0: no one is accessing the file, 1: someone is reading the file, 2: someone is waiting to write in the file
        if mode == 'threads':
            self.read_lock = threading.Lock()  # Protects read_count
            self.write_lock = threading.Lock()  # Ensures mutual exclusion for writing
            # self.readers_lock = threading.Lock()  # To manage readers entering and exiting
        elif mode == 'processes':
            self.read_lock = multiprocessing.Lock()
            self.write_lock = multiprocessing.Lock()
            # self.readers_lock = multiprocessing.Lock()

    def readers_still_reading(self):
        readers_left = False
        for element in self.read_array:
            if element == 0:
                self.read_count += 1
                self.read_array[self.read_count-1] = 2
            elif element == 1:
                readers_left = True
        return readers_left

    def value_set(self, key: object, value: object):
        with self.write_lock:  # only one that can write
            # get all read spaces
            while self.readers_still_reading():
                pass
            super().value_set(key, value)
        # release reading spots
        for i in range(self.max_readers):
            self.read_array[i-1] = 0
        self.read_count = 0  # Reset reader count

    def value_get(self, key):
        with self.read_lock:
            if self.read_count < self.max_readers:
                self.read_count += 1
                self.read_array[self.read_count-1] = 1
            else:
                return "No room for more readers"
        result = super().value_get(key)
        with self.read_lock:
            self.read_count -= 1
            self.read_array[self.read_count-1] = 0
        return result

    def value_delete(self, key):
        with self.write_lock:  # only one that can write
            # get all read spaces
            while self.readers_still_reading():
                pass
            super().value_delete(key)
        # release reading spots
        for i in range(self.max_readers):
            self.read_array[i-1] = 0
        self.read_count = 0  # Reset reader count
