# This class defines a distance graph list and dictionary for the address ID and address.
class DistanceGraph:

    def __init__(self):
        self.distance_list = []
        self.address_list = {}

    # Inserts address ID and address into a dictionary.
    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def insert_al(self, address_id, address):
        self.address_list[address_id] = address

    # Inserts lists containing distances into a list.
    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def insert_dl(self, distances):
        self.distance_list.append(distances)

    # Searches for the address in a dictionary and returns the associated key.
    # Time Complexity: O(N)
    # Space Complexity: O(1)
    def search_address(self, address):
        for key, value in self.address_list.items():
            if address in value:
                return key
