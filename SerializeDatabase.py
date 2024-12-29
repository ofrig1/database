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
        self.file = open('data.pkl', 'wb')

    def value_set(self, key, value):
        """
        Overrides the value_set method from the Database class.
        Sets the key-value pair in the database and then serializes and saves the data.
        :param key: The key under which the value will be stored
        :param value:
        :return:
        """
        result = super().value_set(key, value)
        if result:
            try:
                pickle.dump({key: value}, self.file)  # Serialize the single key-value pair
                logging.info(f"Serialized and saved key-value pair: {key} = {value}")
                self.file.flush()  # Force writing buffered data to disk
            except Exception as e:
                logging.error(f"Failed to save data for key {key}: {e}")
        else:
            logging.error(f"Failed to set value for key: {key}")
        return result

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
            print("Data loaded from data.pkl:", self.data)
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
        # try:
        #     with open('data.pkl', 'rb') as file:
        #         self.data = pickle.load(file)
        #     logging.info("Data loaded from data.pkl: %s", self.data)
        # except FileNotFoundError:
        #     logging.warning("Load failed: data.pkl no t found.")
        # except Exception as e:
        #     logging.error(f"Failed to load data: {e}")

        with open('data.pkl', "rb") as f:
            while True:
                try:
                    loaded_object = pickle.load(f)
                    for k, v in loaded_object.items():
                        self.data[k] = v
                        # self.data[k] = value
                except EOFError:
                    break
