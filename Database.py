class Database:
    def __init__(self):
        self.data = {}

    def value_set(self, key, value):
        self.data[key] = value
        return True

    def value_get(self, key):
        if key in self.data:
            return self.data[key]
        else:
            return None

    def value_delete(self, key):
        if key in self.data:
            self.data.pop(key)
        else:
            return None
