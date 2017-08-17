import argparse
import Algorithms
import Input

if __name__ == '__main__':
    # move to new class
    parser = argparse.ArgumentParser()
    parser.add_argument("algorithm")
    parser.add_argument("--bounds", action="store_true")
    parser.add_argument("--constraints", action="store_true")
    args = parser.parse_args()

    min_int = -2**31
    max_int = 2**31 - 1
    
    min_char = 0x61
    max_char = 0x7a
    
    min_len = 10
    max_len = 10
    
    n_inputs = 26

    if args.bounds:
        val = input("min_int (default -2**31): ")
        if val and type(val) == int:
            min_int = val

        val = input("max_int (default 2**31-1): ")
        if val and type(val) == int:
            max_int = val

        val = input("min_char (default 0x61)")
        if val and len(val) == 1:
            min_char = ord(val)

        val = input("max_char (default 0x7a): ")
        if val and len(val) == 1:
            max_char = ord(val)

        val = input("min_len (default 10): ")
        if val and type(val) == int:
            min_len = val

        val = input("max_len (default 10): ")
        if val and type(val) == int:
            max_len = val

    if args.constraints:
        # TODO: implement arbitrary constraints
        # Limited selection of characters (eg, there could be gaps; range = [A, G] U [J, Z]
        # Ints might have to be prime, multiple or factors of another int, other strange constraints

        pass

    output = None

    # gonna be a big if stack somewhere
    if args.algorithm == "sort":
        algorithm = Algorithms.Sort()
        output = algorithm.exploit(Input.StringGenerator(Input.CharGenerator(min_char, max_char), min_len, max_len), n_inputs)


    # flow networks:
    elif args.algorithm == "fordfulkerson":
        algorithm = Algorithms.FordFulkerson()
        output = algorithm.exploit(Input.IntGenerator(min_int, max_int), n_inputs)

    elif args.algorithm == "pushrelabel":
        algorithm = Algorithms.PushRelabel()
        output = algorithm.exploit(Input.IntGenerator(min_int, max_int), n_inputs)

    elif args.algorithm == "edmondskarp":
        algorithm = Algorithms.EdmondsKarp()
        output = algorithm.exploit(Input.IntGenerator(min_int, max_int), n_inputs)

    # graph Algorithms:
    elif args.algorithm == "dijkstra":
        algorithm = Algorithms.Dijkstra()
        output = algorithm.exploit(Input.StringGenerator(Input.CharGenerator(min_char, max_char), min_len, max_len), n_inputs)

    elif args.algorithm == "fleury":
        algorithm = Algorithms.Fleury()
        output = algorithm.exploit(Input.StringGenerator(Input.CharGenerator(min_char, max_char), min_len, max_len), n_inputs)

    elif args.algorithm == "floydwarshall":
        algorithm = Algorithms.FloydWarshall()
        output = algorithm.exploit(Input.StringGenerator(Input.CharGenerator(min_char, max_char), min_len, max_len), n_inputs)

    elif args.algorithm == "hierholzer":
        algorithm = Algorithms.Hierholzer()
        output = algorithm.exploit(Input.StringGenerator(Input.CharGenerator(min_char, max_char), min_len, max_len), n_inputs)

    elif args.algorithm == "bfs":
        algorithm = Algorithms.BFS()
        output = algorithm.exploit(Input.StringGenerator(Input.CharGenerator(min_char, max_char), min_len, max_len), n_inputs)

    elif args.algorithm == "dfs":
        algorithm = Algorithms.DFS()
        output = algorithm.exploit(Input.StringGenerator(Input.CharGenerator(min_char, max_char), min_len, max_len), n_inputs)


    # finding minimum spanning tree:
    elif args.algorithm == "kruskal":
        algorithm = Algorithms.Kruskal()
        output = algorithm.exploit(Input.IntGenerator(min_int, max_int), n_inputs)

    elif args.algorithm == "prim":
        algorithm = Algorithms.Prim()
        output = algorithm.exploit(Input.IntGenerator(min_int, max_int), n_inputs)


    # string comparison Algorithms:
    elif args.algorithm == "rabinkarp":
        algorithm = Algorithms.RabinKarp()
        output = algorithm.exploit(Input.StringGenerator(Input.CharGenerator(min_char, max_char), min_len, max_len), n_inputs)

    elif args.algorithm == "boyermoore":
        algorithm = Algorithms.BoyerMoore()
        output = algorithm.exploit(Input.StringGenerator(Input.CharGenerator(min_char, max_char), min_len, max_len), n_inputs)


    # Shapes:
    elif args.algorithm == "jarvis":
        algorithm = Algorithms.Jarvis()
        output = algorithm.exploit(Input.IntGenerator(min_int, max_int), n_inputs)

    elif args.algorithm == "graham":
        algorithm = Algorithms.Graham()
        output = algorithm.exploit(Input.IntGenerator(min_int, max_int), n_inputs)

    print(output)
