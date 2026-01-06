class Memory:
    def __init__(self):
        self.short_term = {}
        self.long_term = []

    def set_stm(self, key, value):
        self.short_term[key] = value

    def get_stm(self, key):
        return self.short_term.get(key)

    def clear_stm(self):
        self.short_term = {}

    def store_ltm(self, summary: str):
        self.long_term.append(summary)

    def retrieve_ltm(self):
        return self.long_term
