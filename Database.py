import logging

logging.basicConfig(filename="database.log", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', )


class Database:
    def __init__(self):
        self.data = {}
        logging.info("Database initialized.")

    def value_set(self, key, value):
        self.data[key] = value
        logging.info(f"Set: {key} = {value}")
        return True

    def value_get(self, key):
        if key in self.data:
            logging.info(f"Get: {key} = {self.data[key]}")
            return self.data[key]
        else:
            logging.info(f"Get: {key} = None (key does not exist)")
            return None

    def value_delete(self, key):
        if key in self.data:
            self.data.pop(key)
            logging.info(f"Delete: {key} (successful)")
        else:
            logging.info(f"Delete: {key} (key does not exist)")
            return None
