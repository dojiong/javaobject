

class ReferenceTable:

    class NotFound(Exception):
        pass

    def __init__(self):
        self.table = []
        self.next = 0
        self.reverse_table = {}

    @staticmethod
    def _get_hash(obj):
        hf = getattr(obj, '__hash__', None)
        if callable(hf):
            return hash(obj)
        return id(obj)

    def put(self, obj):
        h = self._get_hash(obj)
        self.table.append(obj)
        idx = self.next
        self.reverse_table[h] = idx
        self.next += 1
        return idx

    def replace(self, idx, newobj):
        del self.reverse_table[self._get_hash(self.table[idx])]
        self.table[idx] = newobj
        self.reverse_table[self._get_hash(newobj)] = idx

    def get(self, idx):
        if idx >= self.next:
            print(self.table)
            raise self.NotFound
        return self.table[idx]

    def reverse(self, obj):
        return self.reverse_table.get(self._get_hash(obj), -1)

    def __contains__(self, obj):
        return self._get_hash(obj) in self.reverse_table
