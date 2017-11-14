#!/usr/bin/python
from lexical import transform
from parsing import parsing
from collections import Counter
import collections
import argparse
import re

parser = argparse.ArgumentParser(description='Expert System: Solver')
parser.add_argument('files', nargs='*')

def main(filename):
	rules = parsing(filename)
	lexical_rules = transform(rules)


if __name__ == "__main__":
	args = parser.parse_args()
	if (len(args.files) >= 1):
		main(args.files[0])
	else:
		print "Incorrect Argument"

# Si on met un \n directement au debut Parsing Error

