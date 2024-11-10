from Database import Database
import pickle
import logging


class SerializeDatabase(Database):
    def __init__(self):
        super().__init__()

    def save(self):
        try:
            with open('data.pkl', 'wb') as file:
                pickle.dump(self.data, file)
            logging.info("Data serialized and saved to data.pkl")
        except Exception as e:
            logging.error(f"Failed to save data: {e}")

    def load(self):
        try:
            with open('data.pkl', 'rb') as file:
                self.data = pickle.load(file)
            logging.info("Data loaded from data.pkl: %s", self.data)
        except FileNotFoundError:
            logging.warning("Load failed: data.pkl not found.")
        except Exception as e:
            logging.error(f"Failed to load data: {e}")
