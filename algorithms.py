from abc import ABC, abstractmethod
import input

class Algorithm(object):
    @abstractmethod
    def exploit(self, generator, n_inputs):
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

# Graph algorithms - return adj matrix (?)

class Dijkstra(Algorithm):
    # Return vertices and edge weights
    # Maybe make values different
    def exploit(self, generator, n_inputs):
        value = generator.get_random() # Just names for nodes...
        weight = generator.get_random()
        V = [value] * n_inputs
        E = [[weight for x in range(n_inputs)] for y in range(n_inputs)]

        return V, E

class FordFulkerson(Algorithm):
    def exploit(self, generator, n_inputs):
        weight = generator.get_max_value()
        E = [[weight for x in range(n_inputs)] for y in range(n_inputs)]
        # Incomplete
        # https://en.wikipedia.org/wiki/Ford%E2%80%93Fulkerson_algorithm#Integral_example

class PushRelabel(Algorithm):
    def exploit(self, generator, n_inputs):
        pass

# Definitely needs to be broadened (Response8.txt, 52)
class RecursiveXML(Algorithm):
    pass

# (Response14.txt, 17, 30, 36, 54 - not really an algorithm I can exploit?)
class Compression(Algorithm):
    pass

# Should return 1+ matrices. Response 34, 50
class MatrixOperations(Algorithm):
    pass

# Response 39
class Exponent(Algorithm):
    pass


class Fleury(Algorithm):
    # this could be slow if n_inputs is large enough
    # TODO: Find a way to modify the constraints of which edges can be made
    def exploit(self, generator, n_inputs):
        G = {}
        possible_nodes = []
        n = "A"
        for i in range(n_inputs):
            possible_nodes.append(n)
            n = generator.get_greater_than(n)
        for i in range(n_inputs):
            for n in range(n_inputs):
                G[possible_nodes[i]] = possible_nodes[n]

        return G


class Hierholzer(Algorithm):
    def exploit(self, generator, n_inputs):
        return Fleury.exploit(generator, n_inputs)


class TopologicalSort(Algorithm):
    def exploit(self, generator, n_inputs):
        pass  # likely the same as the past two


# Minimum spanning tree
class Kruskal(Algorithm):
    pass


class Prim(Algorithm):
    pass


class BFS(Algorithm):
    def exploit(self, generator, n_inputs):
        return Fleury.exploit(generator, n_inputs)


class DFS(Algorithm):
    def exploit(self, generator, n_inputs):
        return Fleury.exploit(generator, n_inputs)


class KCenter(Algorithm):
    def exploit(self, generator, n_inputs):
        pass


# Comparison algorithm
#  occurs when all characters of pattern and text are same as the hash values of all the substrings of txt[] match with hash value of pat[]. For example pat[] = “AAA” and txt[] = “AAAAAAA”.
class RabinKarp(Algorithm):
    def exploit(self, generator, n_inputs):
        whole = generator.get_random() * n_inputs
        pattern = generator.get_random() * int(n_inputs / 2)
        return whole, pattern


class BoyerMoore(Algorithm):
    def exploit(self, generator, n_inputs):
        whole = generator.get_random() * n_inputs
        pattern = generator.get_random() * int(n_inputs / 2)
        return whole, pattern


# Dynamic:



# Data structures:

# There should be a way to indicate/exploit worst case operations
# For instance - union on binary heaps is O(n), where all other operations are either O(log n) or O(1)

class Hashmap(Algorithm):
    pass

class Trie(Algorithm):
    # Worst case - input with as similar input as possible
    def exploit(self, generator, n_inputs):
        output = [generator.get_random()]

        for i in range(1, n_inputs):
            output.append(generator.get_less_than(output[i - 1]))

        return output

class PriorityQueue(Algorithm):
    pass

class BinarySearchTree(Algorithm):
    # Identical to sort
    def exploit(self, generator, n_inputs):
        output = [generator.get_random()]  # pick random value for now, need to check range in future

        for i in range(1, n_inputs):
            output.append(generator.get_less_than(output[i - 1]))

        return output

class AVLTree(Algorithm):
    # Constant insertions can slow it down
    def exploit(self, generator, n_inputs):
        output = [generator.get_random()]  # pick random value for now, need to check range in future

        for i in range(1, n_inputs):
            output.append(generator.get_less_than(output[i - 1]))

        return output

class RedBlackTree(Algorithm):
    pass

# Worst case - as few children on each node as possible
class BTree(Algorithm):
    pass

class BinaryHeap(Algorithm):
    # Merging heaps takes O(n) time (slower than other operations)
    pass

class BinomialHeap(Algorithm):
    pass

class FibonacciHeap(Algorithm):
    # Delete node and delete minimum can take O(n) time
    pass

class Graph(Algorithm):
    # Maybe consider distinction for different graph algorithms
    pass
