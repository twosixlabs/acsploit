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
        output = algorithm.exploit(input.StringGenerator(input.CharGenerator(0x61, 0x7a), 10,10), 27)

    # flow networks:
    elif args.algorithm == "ford fulkerson":
        algorithm = algorithms.FordFulkerson()
        output = algorithm.exploit(input.IntGenerator(0, 2**31-1), 27)
    elif args.algorithm == "push relabel":
        algorithm = algorithms.PushRelabel()
        output = algorithm.exploit(input.IntGenerator(0, 2**31-1), 27)
    elif args.algorithm == "edmonds karp":
        algorithm = algorithms.EdmondsKarp()
        output = algorithm.exploit(input.IntGenerator(0, 2**31-1), 27)

    # graph algorithms:
    elif args.algorithm == "dijkstra":
        algorithm = algorithms.Dijkstra()
        output = algorithm.exploit(input.IntGenerator(0, 2**31-1), 27)
    elif args.algorithm == "fleury":
        algorithm = algorithms.Fleury()
        output = algorithm.exploit(input.IntGenerator(0, 2**31-1), 27)
    elif args.algorithm == "floyd warshall":
        pass
    print(output)
