import argparse
import algorithms
import input

def main():
	#move to new class
	parser = argparse.ArgumentParser()
	parser.add_argument("algorithm")
	args = parser.parse_args()	

	if args.algorithm == "sort":
		algorithm = algorithms.Sort()
		output = algorithm.exploit(input.StringGenerator(input.CharGenerator(0x61, 0x7a), 10,10), 27)
	
	#gonna be a big if stack somewhere
	print(output)

main()


