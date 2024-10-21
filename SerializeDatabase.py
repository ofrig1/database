from Database import Database
import pickle


class SerializeDatabase(Database):
    def __init__(self):
        super().__init__()

    def save(self):
        with open('data.pkl', 'wb') as file:
            pickle.dump(self.data, file)
        print("Data serialized and saved to data.pkl")

    def load(self):
        with open('data.pkl', 'rb') as file:
            self.data = pickle.load(file)
        print("Data loaded from data.pkl:", self.data)
