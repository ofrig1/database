from Database import Database
import pickle
import logging


class SerializeDatabase(Database):
    def __init__(self):
        """
        Initializes the SerializeDatabase by calling the parent Database
        initializer, creating an empty database with serialization capabilities.
        """
        super().__init__()

    def save(self):
        """
        Serializes the current database data and saves it to a file named 'data.pkl'.
        Attempts to save the contents of the database to a file using
        Python's pickle module
        :return: None
        """
        try:
            with open('data.pkl', 'wb') as file:
                pickle.dump(self.data, file)
            logging.info("Data serialized and saved to data.pkl")
        except Exception as e:
            logging.error(f"Failed to save data: {e}")

    def load(self):
        """
        Loads database data from a serialized file named 'data.pkl'
        Attempts to load data from 'data.pkl' to restore the database's
        state. If the file is found and successfully read, the data is loaded and
        a log entry is made indicating the data was loaded.
        :return: None
        """
        try:
            with open('data.pkl', 'rb') as file:
                self.data = pickle.load(file)
            logging.info("Data loaded from data.pkl: %s", self.data)
        except FileNotFoundError:
            logging.warning("Load failed: data.pkl not found.")
        except Exception as e:
            logging.error(f"Failed to load data: {e}")
