import time

from SerializeDatabase import SerializeDatabase
import threading
import multiprocessing
import logging

MAX = 10


class SyncDatabase(SerializeDatabase):
    def __init__(self, mode='threads'):
        super().__init__()
        self.mode = mode
        self.max_readers = MAX
        self.read_count = 0
        self.read_array = [0]*MAX
        # 0: no one is accessing the file, 1: someone is reading the file, 2: someone is waiting to write in the file
        if mode == 'threads':
            self.read_lock = threading.Lock()  # Protects read_count
            self.write_lock = threading.Lock()  # Ensures mutual exclusion for writing
            # self.readers_lock = threading.Lock()  # To manage readers entering and exiting
        elif mode == 'processes':
            self.read_lock = multiprocessing.Lock()
            self.write_lock = multiprocessing.Lock()
            # self.readers_lock = multiprocessing.Lock()
        logging.info(f"SyncDatabase initialized in {self.mode} mode with max readers {self.max_readers}")

    def readers_still_reading(self):
        readers_left = False
        for element in self.read_array:
            if element == 0: # empty
                self.read_count += 1
                logging.debug("num of readers: " + str(self.read_count))
                self.read_array[self.read_count-1] = 2  # WRITE
            elif element == 1:
                readers_left = True
        logging.debug(f"Readers still reading: {self.read_count}")
        return readers_left

    def value_set(self, key: object, value: object):
        logging.debug(f"Attempting to set key '{key}' with value '{value}'")
        with self.write_lock:  # only one that can write
            # get all read spaces
            while self.readers_still_reading():
                pass
            super().value_set(key, value)
            logging.info(f"Set key '{key}' with value '{value}'")
        # release reading spots
        for i in range(self.max_readers):
            self.read_array[i-1] = 0
        self.read_count = 0  # Reset reader count

    def value_get(self, key):
        index = 0
        with self.read_lock:
            logging.debug(f"Attempting to get key '{key}' and current number of readers is '{self.read_count}")
            # time.sleep(1)
            if self.read_count < self.max_readers:
                self.read_count += 1
                index = self.read_count-1
                self.read_array[index] = 1
            else:
                logging.warning("Max readers reached, unable to add more readers.")
                return "No room for more readers"
        result = super().value_get(key)
        if result is not None:
            logging.info(f"Retrieved key '{key}' with value '{result}'")
        else:
            logging.warning(f"Key '{key}' not found.")

        with self.read_lock:
            self.read_count -= 1
            self.read_array[index] = 0
        return result

    def value_delete(self, key):
        logging.debug(f"Attempting to delete key '{key}'")
        with self.write_lock:  # only one that can write
            # get all read spaces
            while self.readers_still_reading():
                pass
            super().value_delete(key)
        logging.info(f"Deleted key '{key}' (if it existed)")
        # release reading spots
        for i in range(self.max_readers):
            self.read_array[i-1] = 0
        self.read_count = 0  # Reset reader count
