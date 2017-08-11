import argparse
import algorithms
import input

if __name__ == '__main__':
    # move to new class
    parser = argparse.ArgumentParser()
    parser.add_argument("algorithm")
    args = parser.parse_args()

    output = None

    # gonna be a big if stack somewhere
    if args.algorithm == "sort":
        algorithm = algorithms.Sort()
        output = algorithm.exploit(input.StringGenerator(input.CharGenerator(0x61, 0x7a), 10, 10), 26)


    # flow networks:
    elif args.algorithm == "fordfulkerson":
        algorithm = algorithms.FordFulkerson()
        output = algorithm.exploit(input.IntGenerator(0, 2**31-1), 26)

    elif args.algorithm == "pushrelabel":
        algorithm = algorithms.PushRelabel()
        output = algorithm.exploit(input.IntGenerator(0, 2**31-1), 26)

    elif args.algorithm == "edmondskarp":
        algorithm = algorithms.EdmondsKarp()
        output = algorithm.exploit(input.IntGenerator(0, 2**31-1), 26)


    # graph algorithms:
    elif args.algorithm == "dijkstra":
        algorithm = algorithms.Dijkstra()
        output = algorithm.exploit(input.StringGenerator(input.CharGenerator(0x61, 0x7a), 10, 10), 26)

    elif args.algorithm == "fleury":
        algorithm = algorithms.Fleury()
        output = algorithm.exploit(input.StringGenerator(input.CharGenerator(0x61, 0x7a), 10, 10), 26)

    elif args.algorithm == "floydwarshall":
        algorithm = algorithms.FloydWarshall()
        output = algorithm.exploit(input.StringGenerator(input.CharGenerator(0x61, 0x7a), 10, 10), 26)

    elif args.algorithm == "hierholzer":
        algorithm = algorithms.Hierholzer()
        output = algorithm.exploit(input.StringGenerator(input.CharGenerator(0x61, 0x7a), 10, 10), 26)

    elif args.algorithm == "bfs":
        algorithm = algorithms.BFS()
        output = algorithm.exploit(input.StringGenerator(input.CharGenerator(0x61, 0x7a), 10, 10), 26)

    elif args.algorithm == "dfs":
        algorithm = algorithms.DFS()
        output = algorithm.exploit(input.StringGenerator(input.CharGenerator(0x61, 0x7a), 10, 10), 26)


    # finding minimum spanning tree:
    elif args.algorithm == "kruskal":
        algorithm = algorithms.Kruskal()
        output = algorithm.exploit(input.IntGenerator(0, 2 ** 3101), 26)

    elif args.algorithm == "prim":
        algorithm = algorithms.Prim()
        output = algorithm.exploit(input.IntGenerator(0, 2 ** 3101), 26)


    # string comparison algorithms:
    elif args.algorithm == "rabinkarp":
        algorithm = algorithms.RabinKarp()
        output = algorithm.exploit(input.StringGenerator(input.CharGenerator(0x61, 0x7a), 10, 10), 26)

    elif args.algorithm == "boyermoore":
        algorithm = algorithms.BoyerMoore()
        output = algorithm.exploit(input.StringGenerator(input.CharGenerator(0x61, 0x7a), 10, 10), 26)


    print(output)
