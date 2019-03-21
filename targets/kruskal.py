import argparse


def kruskal(edges):
    tree = []
    operations = 0
    # stores the set of vertices reachable from each vertex
    # by the edges currently in the tree
    vertex_sets = [{i} for i in range(len(edges))]

    # make a sorted list of each edge
    # stored as a tuple of (vertex, vertex, weight)
    sorted_edges = []
    for i in range(len(edges)):
        # edges[i][j] == edges[j][i]
        # edges[i][i] == 0
        for j in range(i+1, len(edges)):
            sorted_edges.append((i, j, edges[i][j]))
    sorted_edges.sort(key=lambda x: x[2])

    for edge in sorted_edges:
        operations += 1
        u, v, _ = edge
        if vertex_sets[u] != vertex_sets[v]:  # this seems to be wrong…
            tree.append(edge)
            union = vertex_sets[u] | vertex_sets[v]
            for vertex in union:
                vertex_sets[vertex] = union

    return tree, operations


def print_tree(tree):
    for edge in tree:
        print('%i <-> %i (weight %i)' % edge)


def load_graph(graph_filename):
    # each line of the is a []-bracketed list
    # the file unpacks to a n x n array
    # the i,j-th element is the cost of the edge between i and j
    # the graph is undirected so a[i][j] == a[j][i]
    # a[i][j] == 0 means no edge between i and j
    edges = []
    with open(graph_filename) as graph_file:
        for line in graph_file.readlines():
            edges.append([int(i) for i in line[1:-2].split(', ')])
    return edges


def main():
    parser = argparse.ArgumentParser(description='Implementation of Kruskal\'s algorithm for finding a minimum spanning tree to demonstrate ACsploit')
    parser.add_argument('graph', help='File containing the adjacency matrix of an undirected weighted graph')
    args = parser.parse_args()

    graph = load_graph(args.graph)

    tree, operations = kruskal(graph)

    print('The minimum spanning tree is:')
    print_tree(tree)
    print('%i operations were performed on the %i-vertex input graph' % (operations, len(graph)))


if __name__ == '__main__':
    main()
