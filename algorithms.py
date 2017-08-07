from abc import ABC, abstractmethod
import input

class Algorithm(object):
    @abstractmethod
    def exploit(self, generator):
        pass

class Sort(Algorithm):
    # TODO
    # 1. ascending vs descending
    # 2. what if there are not enough values (n > range)
    def exploit(self, generator, n_inputs):
        output = [generator.get_random()] # pick random value for now, need to check range in future

        for i in range(1,n_inputs):
            output.append(generator.get_less_than(output[i-1]))

        return output

# Data structures:

# There should be a way to indicate worst case operations
# For instance - union on binary heaps is O(n), where all other operations are either O(log n) or O(1)

class Hashmap(Algorithm):
    pass

class Trie(Algorithm):
    pass

class BinarySearchTree(Algorithm):
    pass

class RedBlackTree(Algorithm):
    pass

class BTree(Algorithm):
    pass

class BinomialHeap(Algorithm):
    pass

class FibonacciHeap(Algorithm):
    pass

class Graph(Algorithm):
    # Maybe consider distinction for different graph algorithms
    pass


