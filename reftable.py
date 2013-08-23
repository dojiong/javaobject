

class ReferenceTable:

    class NotFound(Exception):
        pass

    def __init__(self):
        self.table = []
        self.next = 0
        self.reverse = {}

    def put(self, obj):
        self.table.append(obj)
        idx = self.next
        self.next += 1
        return idx

    def replace(self, idx, newobj):
        self.table[idx] = newobj

    def get(self, idx):
        if idx >= self.next:
            raise self.NotFound
        return self.table[idx]

    def reverse(self, obj):
        return self.reverse.get(obj, -1)
