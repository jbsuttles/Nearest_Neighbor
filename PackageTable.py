# This class defines a hash table for packages.
class PackageTable:

    # Constructor
    def __init__(self):
        self.size = 40
        self.table = [None] * self.size

    # Generate Hash Key.
    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def _hash(self, key):
        return key % self.size

    # Insert Key (Package ID) and associated values into hash table.
    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def insert(self, key, value):
        bucket = self._hash(key)
        key_value = [key, value]

        if self.table[bucket] is None:
            self.table[bucket] = list([key_value])
            return True
        else:
            return False

    # Insert address ID into values. Address ID is associated with the address from DistanceGraph dictionary that
    # matches that address from PackageTable hash table.
    # Time Complexity: O(N)
    # Space Complexity: O(1)
    def insert_addressID(self, key, add_id):
        bucket = self._hash(key)

        if self.table[bucket] is not None:
            for value in self.table[bucket]:
                if value[0] == key:
                    value[1].append(add_id)

    # Search for the Key(Package ID) and returns the associated value if found.
    # Time Complexity: O(N)
    # Space Complexity: O(1)
    def search(self, key):
        bucket = self._hash(key)
        if self.table[bucket] is not None:
            for value in self.table[bucket]:
                if value[0] == key:
                    return value[1]
                else:
                    return None
