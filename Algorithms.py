# from abc import ABC
from abc import abstractmethod
import random
import math

class Algorithm(object):
    @abstractmethod
    def exploit(self, generator, n_inputs):
        pass

class Sort(Algorithm):
    # TODO
    # 1. ascending vs descending
    # 2. what if there are not enough values (n > range)
    def exploit(self, generator, n_inputs):
        output = [generator.get_random()]  # pick random value for now, need to check range in future

        for i in range(1,n_inputs):
            output.append(generator.get_less_than(output[i-1]))

        return output

# Flow networks:

class FordFulkerson(Algorithm):
    def exploit(self, generator, n_inputs):
        heavy = generator.get_max_value()
        light = 1
        G = {}
        possible_nodes = []
        n = "A"  # Maybe should be generator.get_min_value()
        for i in range(n_inputs):
            possible_nodes.append(n)
            n = generator.get_greater_than(n)
        for i in range(1, n_inputs-1):
            G[possible_nodes[i]] = (set(), light)
            for j in range(1, n_inputs - 1):
                G[possible_nodes[i]][0].add(possible_nodes[j])
        G[possible_nodes[0]] = (set(), heavy)
        for i in range(n_inputs):
            G[possible_nodes[0]][0].add(possible_nodes[i])
        return G
        # https://en.wikipedia.org/wiki/Ford%E2%80%93Fulkerson_algorithm#Integral_example

class Dinic(Algorithm):
    def exploit(self, generator, n_inputs):
        return Kruskal.exploit(Kruskal(), generator, n_inputs)

class PushRelabel(Algorithm):  # O(V^2 * E)
    def exploit(self, generator, n_inputs):
        return Kruskal.exploit(Kruskal(), generator, n_inputs)

class EdmondsKarp(Algorithm): # O(V * E^2)
    def exploit(self, generator, n_inputs):
        return Kruskal.exploit(Kruskal(), generator, n_inputs)

# Directly from engagement problms:
# TODO: Go through engagement problems

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

# Graph algorithms - return adj matrix (?)

class Fleury(Algorithm):
    # this could be slow if n_inputs is large enough
    # TODO: Find a way to modify the constraints of which edges can be made
    def exploit(self, generator, n_inputs):
        G = {}
        possible_nodes = []
        n = "A"
        for i in range(n_inputs):
            possible_nodes.append(n)
            G[n] = set()
            n = generator.get_greater_than(n)
        for i in range(n_inputs):
            for n in range(n_inputs):
                G[possible_nodes[i]].add(possible_nodes[n])
        return G

class Dijkstra(Algorithm):
    def exploit(self, generator, n_inputs):
        return Kruskal.exploit(Kruskal(), generator, n_inputs)

class BellmanFord(Algorithm):
    def exploit(self, generator, n_inputs):
        return Kruskal.exploit(Kruskal(), generator, n_inputs)

class FloydWarshall(Algorithm):
    def exploit(self, generator, n_inputs):
        return Kruskal.exploit(Kruskal(), generator, n_inputs)

class Johnson(Algorithm):
    def exploit(self, generator, n_inputs):
        return Fleury.exploit(Fleury(), generator, n_inputs)

class Hierholzer(Algorithm):
    def exploit(self, generator, n_inputs):
        return Fleury.exploit(Fleury(), generator, n_inputs)

class TopologicalSort(Algorithm):
    def exploit(self, generator, n_inputs):
        return Fleury.exploit(Fleury(), generator, n_inputs)

# A 'complete' graph might actually make these a lot faster...
class BFS(Algorithm):
    def exploit(self, generator, n_inputs):
        return Fleury.exploit(Fleury(), generator, n_inputs)

class DFS(Algorithm):
    def exploit(self, generator, n_inputs):
        # Actually might be different
        return Fleury.exploit(Fleury(), generator, n_inputs)

# Minimum spanning tree
# Weighted graphs represented G = {0 -> {1 -> 0.7, 2 -> 1.5} , ...}
class Kruskal(Algorithm):
    def exploit(self, generator, n_inputs):
        G = {}
        weight = 1
        possible_nodes = []
        n = "A"
        for i in range(n_inputs):
            possible_nodes.append(n)
            n = generator.get_greater_than(n)
        for i in range(n_inputs):
            G[possible_nodes[i]] = []
            for n in range(n_inputs):
                G[possible_nodes[i]].append((possible_nodes[n], weight))
        return G


class Prim(Algorithm):
    def exploit(self, generator, n_inputs):
        return Kruskal.exploit(Kruskal(), generator, n_inputs)


class KCenter(Algorithm):
    def exploit(self, generator, n_inputs):
        pass

# Comparison algorithms

class RabinKarp(Algorithm):
    def exploit(self, generator, n_inputs):
        base = generator.get_random()[0]
        whole = base * n_inputs
        pattern = base * int(n_inputs / 2)
        return whole, pattern


class BoyerMoore(Algorithm):
    def exploit(self, generator, n_inputs):
        base = generator.get_random()[0]
        whole = base * n_inputs
        pattern = base * int(n_inputs / 2)
        return whole, pattern

# Shapes:

class Jarvis(Algorithm):
    def exploit(self, generator, n_inputs):
        # Generate n points on a polygon, to force all points to lie on a hull -> worse case O(n^2)
        angles = []
        points = []
        x0 = y0 = (generator.get_max_value() + generator.get_min_value()) / 2
        R = generator.get_random() / 2  # Need to be very careful with getting random (could go out of bounds)
        for n in range(n_inputs):
            angles.append(random.random() * 2 * math.pi)

        list.sort(angles)

        for n in range(n_inputs):
            x = x0 + R * math.cos(angles[n])
            y = y0 + R * math.sin(angles[n])
            points.append((int(x), int(y)))

        return points


class Graham(Algorithm):  # Might not be a terrible worst case - just O(n*log(n))
    def exploit(self, generator, n_inputs):
        return Jarvis.exploit(Jarvis(), generator, n_inputs)

# Need to be categorized:


class HopcroftKarp(Algorithm):
    def exploit(self, generator, n_inputs):
        left = []
        right = []
        n = generator.get_min_value()
        for i in range(int(n_inputs/2)):
            left.append(n)
            n = generator.get_greater_than(n)
            right.append(n)
            n = generator.get_greater_than(n)
        G = {}
        for i in range(len(left)):
            G[left[i]] = []
            G[right[i]] = []
            for n in range(len(right)):
                G[left[i]].append(right[n])
                G[right[i]].append(left[n])  # Redundant list -> should make sure all graphs are either redundant or not
        return G

# Dynamic:


# Data structures:

# There should be a way to indicate/exploit worst case operations
# For instance - union on binary heaps is O(n), where all other operations are either O(log n) or O(1)

class Hashmap(Algorithm):
    def exploit(self, generator, n_inputs):
        keys = []
        base = generator.get_random()
        hash = self.get_hash_function()

        for i in range(n_inputs):
            # TODO: Figure out how to generate values -> same hash
            value = 0
            if hash(value) == hash(base):
                keys.append(value)
            else:
                pass
                # try again

        return keys

    def get_hash_function(self):
        return int

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
    def exploit(self, generator, n_inputs):
        pass

# Worst case - as few children on each node as possible
class BTree(Algorithm):
    def exploit(self, generator, n_inputs):
        pass

class BinaryHeap(Algorithm):
    # Merging heaps takes O(n) time (slower than other operations)
    def exploit(self, generator, n_inputs):
        pass

class BinomialHeap(Algorithm):
    def exploit(self, generator, n_inputs):
        pass

class FibonacciHeap(Algorithm):
    # Delete minimum takes O(n) time
    def exploit(self, generator, n_inputs):
        pass
