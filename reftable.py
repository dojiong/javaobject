

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
        self.reverse_table[obj] = idx
        self.next += 1
        return idx

    def replace(self, idx, newobj):
        del self.reverse_table[self.table[idx]]
        self.table[idx] = newobj
        self.reverse_table[newobj] = idx

    def get(self, idx):
        if idx >= self.next:
            raise self.NotFound
        return self.table[idx]

    def reverse(self, obj):
        return self.reverse_table.get(obj, -1)

    def __contains__(self, obj):
        return obj in self.reverse_table
