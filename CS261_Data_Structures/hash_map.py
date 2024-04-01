# Name: Christopher Felt
# OSU Email: feltc@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Project 7
# Due Date: 03 Dec 2021
# Description: Implementation of a Hash Map Abstract Data Type with collision resolution using chaining.


# Import pre-written DynamicArray and LinkedList classes
from a7_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        Replace the contents of each bucket that contains a node(s) with an
        empty linked list and set hash map size to 0. Return nothing.
        """
        # set index counter to 0
        ind = 0

        # iterate through buckets
        while ind < self.buckets.length():
            # save length of the linked list in the bucket
            ll_size = self.buckets.get_at_index(ind).length()

            # if the bucket is not empty, replace it with an empty LL
            if ll_size != 0:
                self.buckets.set_at_index(ind, LinkedList())
                # reduce size of hash map by number of nodes removed
                self.size -= ll_size

            ind += 1  # next index

    def get(self, key: str) -> object:
        """
        Returns the value of the first node found that matches the given key.
        If no match is found, returns nothing.
        """
        # check if the hash map is empty
        if self.size == 0:
            return None

        # generate hash value from key
        key_hash = self.hash_function(key)
        # convert hash value to index
        index = key_hash % self.buckets.length()

        # find bucket at index and check through the bucket to see if it contains the key
        key_node = self.buckets.get_at_index(index).contains(key)

        # if bucket does not contain key, return None
        if key_node is None:
            return None

        # return key value if bucket contains key
        else:
            return key_node.value

    def put(self, key: str, value: object) -> None:
        """
        Adds the given key:value pair to the hash map as a node at the
        hashed index using the hash function. Increase hash map size by 1.
        """
        # return nothing and exit method if capacity is 0
        if self.capacity == 0:
            return None

        # generate hash value from key
        key_hash = self.hash_function(key)
        # convert hash value to index
        index = key_hash % self.buckets.length()

        # find bucket at index
        bucket = self.buckets.get_at_index(index)

        # if bucket is empty, insert key value pair
        if bucket.length() == 0:
            bucket.insert(key, value)
            self.size += 1
            return None

        # check through the bucket to see if it contains the key
        replace_node = bucket.contains(key)

        # if bucket does not contain key, insert key value pair
        if replace_node is None:
            bucket.insert(key, value)
            self.size += 1
            return None

        # if the bucket DOES contain the key, replace only the value in that node
        else:
            replace_node.value = value
            return None

    def remove(self, key: str) -> None:
        """
        Checks the hash map for the first node that matches the given
        key and removes it if one is found. Reduce hash map size by 1.
        Returns nothing.
        """
        # check if the hash map is empty
        if self.size == 0:
            return None

        # generate hash value from key
        key_hash = self.hash_function(key)
        # convert hash value to index
        index = key_hash % self.buckets.length()

        # find bucket at index and remove key if it exists (remove() returns True if it does, False otherwise)
        key_node = self.buckets.get_at_index(index).remove(key)

        # decrease hash map size if key was removed
        if key_node is True:
            self.size -= 1

    def contains_key(self, key: str) -> bool:
        """
        Checks the hash map for the first node that matches the
        given key. If one is found, returns True. Otherwise, return False.
        """
        # if hash map is empty, does not contain key
        if self.size == 0:
            return False

        # generate hash value from key
        key_hash = self.hash_function(key)
        # convert hash value to index
        index = key_hash % self.buckets.length()

        # check if bucket at index contains the key. if it does, return True. Otherwise, return False
        if self.buckets.get_at_index(index).contains(key) is not None:
            return True
        else:
            return False

    def empty_buckets(self) -> int:
        """
        Counts the number of buckets in the hash map that do not contain
        any nodes with data and returns that number.
        """
        # set index and empty counter to 0
        ind = 0
        empty_count = 0

        # iterate through buckets
        while ind < self.buckets.length():

            # if the bucket is empty, increase empty count by 1
            if self.buckets.get_at_index(ind).length() == 0:
                empty_count += 1

            ind += 1  # next index

        return empty_count  # total number of empty buckets

    def table_load(self) -> float:
        """
        Calculates and returns the load factor of the hash map
        (i.e. total number of elements/number of buckets).
        """
        # hash table load factor = total number of elements/number of buckets
        return self.size / self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        Given a new capacity that is >= 1, replaces the current hash map
        with a new hash map of the given capacity containing all of the
        same key:value pairs with indices rehashed based on the new capacity.
        Returns nothing.
        """
        # do nothing if new capacity < 1
        if new_capacity < 1:
            return None

        # create new hashmap
        temp_hm = DynamicArray()

        # add linked lists to new da until it reaches new capacity
        while temp_hm.length() < new_capacity:
            temp_hm.append(LinkedList())

        # bookmark current index
        cur_ind = 0

        # iterate through current hashmap and add the contents of each bucket to the new hashmap
        while cur_ind < self.capacity:
            # save contents of current bucket
            cur_bucket = self.buckets.get_at_index(cur_ind)

            # if bucket contains anything, add its contents to the new hashmap
            if cur_bucket.length() != 0:
                # iterate through linked list using iterator
                for node in cur_bucket:
                    # generate hash value from key
                    key_hash = self.hash_function(node.key)
                    # convert hash value to index
                    new_ind = key_hash % new_capacity

                    # add node at the new index in the new hashmap
                    temp_hm.get_at_index(new_ind).insert(node.key, node.value)

            cur_ind += 1

        # overwrite current hashmap buckets with new hashmap buckets and update capacity
        self.buckets = temp_hm
        self.capacity = temp_hm.length()

    def get_keys(self) -> DynamicArray:
        """
        Finds all keys in the hash map and returns them in a
        new DynamicArray object.
        """
        # create temporary da
        temp_da = DynamicArray()

        # bookmark current index
        cur_ind = 0

        # iterate through current hashmap and add the contents of each bucket to the new hashmap
        while cur_ind < self.capacity:
            # save contents of current bucket
            cur_bucket = self.buckets.get_at_index(cur_ind)

            # if bucket contains anything, add its contents to the new hashmap
            if cur_bucket.length() != 0:
                # iterate through linked list using iterator
                for node in cur_bucket:
                    # append key to temp da
                    temp_da.append(node.key)

            cur_ind += 1

        # return da containing keys
        return temp_da


# BASIC TESTING
if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())


    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(50, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))


    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)


    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))


    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)


    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'), m.size)
    m.put('key1', 10)
    print(m.get('key1'), m.size)
    m.remove('key1')
    print(m.get('key1'), m.size)
    m.remove('key4')


    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))


    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))


    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
