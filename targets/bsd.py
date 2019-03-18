import argparse


HASH_TABLE_SIZE = 10


class BSDTable:
    def __init__(self):
        self.table = {i: list() for i in range(HASH_TABLE_SIZE)}
        self.collisions = 0  # number of collisions during insert
        self.traversal_time = 0  # time spent looking through lists when retrieving items

    def insert(self, value):
        h = self._hash(value)
        self.table[h].append(value)
        chain_length = len(self.table[h])
        if chain_length > 1:
            self.collisions += 1
            self.traversal_time += chain_length

    def _hash(self, value):
        checksum = 0
        for byte in value:
            checksum = (checksum >> 1) + ((checksum & 1) << 15)
            checksum += ord(byte)
            checksum &= 0xffff
        checksum %= HASH_TABLE_SIZE
        print('Hashed %s to %i' % (value, checksum))
        return checksum


def main():
    parser = argparse.ArgumentParser(description='Implementation of a hash table of size 10 with separate chaining using the BSD hash function to demonstrate ACsploit')
    parser.add_argument('value', metavar='VALUE', nargs='+', help='Values to add to the hash table')
    args = parser.parse_args()

    table = BSDTable()
    for value in args.value:
        table.insert(value)

    print('Inserted %i values, resulting in %i collisions' % (len(args.value), table.collisions))
    print('The average lookup for a value will be %.2f operations (1 is optimal)' % (float(table.traversal_time) / len(args.value)))


if __name__ == '__main__':
    main()
