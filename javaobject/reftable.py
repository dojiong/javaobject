

class ReferenceTable:

    class NotFound(Exception):
        pass

    def __init__(self):
        self.table = []
        self.next = 0
        self.reverse_table = {}

    def put(self, obj):
        self.table.append(obj)
        idx = self.next
        self.reverse_table[id(obj)] = idx
        self.next += 1
        return idx

    def replace(self, idx, newobj):
        del self.reverse_table[id(self.table[idx])]
        self.table[idx] = newobj
        self.reverse_table[id(newobj)] = idx

    def get(self, idx):
        if idx >= self.next:
            raise self.NotFound
        return self.table[idx]

    def reverse(self, obj):
        return self.reverse_table.get(id(obj), -1)

    def __contains__(self, obj):
        return id(obj) in self.reverse_table
