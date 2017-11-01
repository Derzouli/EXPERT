#!/usr/bin/python

from pyparsing import Group, Literal, Optional, Regex, Word, ZeroOrMore, Upcase, alphas, Forward
from collections import Counter
from pyparsing import ParseException
import argparse
import sys
import re

def grammar():
	_and = Literal('+').setParseAction(lambda:'+')
	_not = Literal('!').setParseAction(lambda:'!')
	_or =  Literal('|').setParseAction(lambda:'|')
	_xor =  Literal('^').setParseAction(lambda:'^')
	lpar = Literal("(").suppress()
	rpar = Literal(")").suppress()
	polynomial = Forward()
	sign = _and | _or | _xor
	letter = Upcase(Word(alphas, max=1))
	atom = letter
	monomial = Optional(_not) + atom + Optional(sign) | (lpar + polynomial + rpar)
	polynomial << Group(monomial + ZeroOrMore(monomial))
	return polynomial('left') + '=>' + polynomial('right')

_grammar = grammar()

class Rules(object):

	def __init__(self):
		self.data = {}
		self.count = 0
		self.character = [chr(ord('A')+x) for x in range(26)]
		self.temp = dict((el, 0) for el in self.character)
		self.goal = {}

	def parse(self, s):
		try:
			s_with_blank = ''.join(s.split())
			if (s_with_blank.find('<=>') > 0):
				str_temp = s_with_blank.replace("<=>", "=>")
				stack = []
				equation = _grammar.parseString(str_temp)
				stack.extend(equation.left[0].asList())
				stack.extend(["=>"])
				stack.extend(equation.right[0].asList())
				self.data.update({self.count:stack})
				self.count += 1;
				stack = []
				stack.extend(equation.right[0].asList())
				stack.extend(["=>"])
				stack.extend(equation.left[0].asList())
				self.data.update({self.count:stack})
				self.count += 1;
			else:
				equation = _grammar.parseString(s_with_blank)
				stack = []
				stack.extend(equation.left[0].asList())
				stack.extend(["=>"])
				stack.extend(equation.right[0].asList())
				self.data.update({self.count:stack})
				self.count += 1;
		except ParseException:
			print "Parsing Error"
			sys.exit()

	def set_initial(self, line):
		for c in line:
			if (c.isupper() and c.isalpha()):
				self.temp[c] = 1

	def set_goal(self, line):
		for c in line:
			if (c.isupper() and c.isalpha()):
				self.goal[c] = 1


parser = argparse.ArgumentParser(description='Expert System: Solver')
parser.add_argument('files', nargs='*')

def main(filename):
	rules = Rules()
	file = open(filename, "r")
	for line in file.readlines():
		sharp_pos = line.find("#")
		equal_pos = line.find("=")
		mark_pos = line.find("?")
		len_line = len(line)
		if (len_line == 1):
			continue
		else:
			if (equal_pos == 0):
				rules.set_initial(line[1:])
			if (mark_pos == 0):
				rules.set_goal(line[1:])
			if (equal_pos < 0 and mark_pos < 0) or \
			(equal_pos > 0 and mark_pos < 0) :
				if (sharp_pos > 0):
					rules.parse(line.split("#")[0])
				elif (sharp_pos < 0):
					rules.parse(line)
	if (len(rules.goal) == 0):
		print "No Goal"
		sys.exit()
	if (len(rules.data) == 0):
		print "No Rule"
		sys.exit()
	print rules.data

if __name__ == "__main__":
	args = parser.parse_args()
	if (len(args.files) >= 1):
		main(args.files[0])
	else:
		print "Incorrect Argument"

# Si on met un \n directement au debut Parsing Error

