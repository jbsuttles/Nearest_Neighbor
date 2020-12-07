"""
Simple Hash Table Implementaion with Linear probing
to resolve collision
"""

class HashTable(object):
    """
    HashTable with fixed size and integer keys.
    """
    def __init__(self):
        self.__size = 97
        self._key=[]
        self.__keys = [None] * self.__size
        self.__data = [None] * self.__size

    def set(self,key,data):
        """
        Insert new (Key, value) pair or update existing key.
        """
        hash_index = self.__hashfunction(key)

        if self.__keys[hash_index] == None:
            self._key.append(key)
            self.__keys[hash_index] = key
            self.__data[hash_index] = data

        elif self.__keys[hash_index] == key:
            self.__data[hash_index] = data

        else:
            next_ind = self.__rehash(hash_index)
            while ( self.__keys[next_ind] != None and
                    self.__keys[next_ind] != key) :
                next_ind = self.__rehash(next_ind)

            if self.__keys[next_ind] == None:
                self._key.append(key)
                self.__keys[next_ind]=key
                self.__data[next_ind]=data
            else:
                self.__data[next_ind] = data

    def __hashfunction(self,key):
        """
        Hash value of given key.
        """
        return key%self.__size

    def __rehash(self, hashvalue):
        """
        Rehash to resolve collision.
        """
        return (hashvalue+1)%self.__size

    def get(self,key):
        """
        Return the value if given key is present.
        """
        start_index = self.__hashfunction(key)
        data = None
        position = start_index
        while True:
            if self.__keys[position] == key:
                data = self.__data[position]
                break
            else:
                position=self.__rehash(position)
                if position == start_index:
                    break
        return data

    def pop(self, key):
        """
        Delete and return the value if key is present.
        """
	data = self.get(key)
	if data:
            self._key.remove(key)
            ind = self.__keys.index(key)
            self.__keys[ind] = None
            self.__data[ind] = None
            return data
	else:
            raise KeyError(key)

    def items(self):
        """
        return (key,value) pairs.
        """
	return '[ ' + ', '.join(['['+ str(key) + ',' + str(self.get(key)) + ']' for key in self._key]) + ' ]'

    def __getitem__(self,key):
        return self.get(key)

    def __setitem__(self,key,data):
        self.set(key,data)

    def keys(self):
	return self._key

    def __delitem__(self, key):
	return self.pop(key)

    def __repr__(self):
        return '{ ' + ', '.join([str(key) + ':' + str(self.get(key)) for key in self._key]) + ' }'
