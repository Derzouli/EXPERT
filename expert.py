#!/usr/bin/python

from pyparsing import Group, Literal, Optional, Regex, Word, ZeroOrMore, Upcase, alphas, Forward
from collections import Counter
from pyparsing import ParseException
import collections
import argparse
import sys
import re

def flatten(lst):
	for x in lst:
		if isinstance(x, list):
			for x in flatten(x):
				yield x
		else:
			yield x

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

class Term(object):

	def __init__(self, name, value=False):
		self.name = name
		self.value = value

	def __str__(self):
		return self.name

	def __add__(self, other):
		return Term(self.name + "+" + other.name, self.value & other.value)

	def __xor__(self, other):
		return Term(self.name + "^" + other.name, self.value ^ other.value)

	# Des quon trouve une inversion on inverse
	def __invert__(self):
		return Term("!" + self.name, not self.value)

	# Relation de transitivite OK
	def __eq__(self, other):
		return self.value == other.value and set(self.name.split("+")) == set(other.name.split("+")) \
		and len(self.name) == len(other.name)



class Rules(object):

	def __init__(self):
		self.count = 0
		self.data = []
		self.graph = {}
		self.character = [chr(ord('A')+x) for x in range(26)]
		self.initial_fact = ""
		self.goals = ""
		self.fact = ""

	def parse(self, s):
		try:
			s_with_blank = ''.join(s.split())
			if (s_with_blank.find('<=>') > 0):
				str_temp = s_with_blank.replace("<=>", "=>")
				equation = _grammar.parseString(str_temp)
				match = filter(lambda x : x.isupper() and x.isalpha(), str(equation))
				self.fact += str(match)
				self.data.append((equation.left[0].asList(), equation.right[0].asList()))
				self.data.append((equation.right[0].asList(), equation.left[0].asList()))
			else:
				equation = _grammar.parseString(s_with_blank)
				match = filter(lambda x : x.isupper() and x.isalpha(), str(equation))
				self.fact += str(match)
				self.data.append((equation.left[0].asList(), equation.right[0].asList()))
		except ParseException:
			print "Parsing Error"
			sys.exit()

	def set_initial_facts(self, line):
		for c in line:
			if (c.isupper() and c.isalpha()):
				self.initial_fact += c

	def set_goals(self, line):
		for c in line:
			if (c.isupper() and c.isalpha()):
				self.goals += c

	def search_goal(self, c):
		for key, val in self.data.items():
			if list(flatten(val["right"])).__contains__(c):
				print c

	def resolver(self):
		for c in self.goal:
			self.search_goal(c)


parser = argparse.ArgumentParser(description='Expert System: Solver')
parser.add_argument('files', nargs='*')

def parsing(filename):
	rules = Rules();
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
				rules.set_initial_facts(line[1:])
			if (mark_pos == 0):
				rules.set_goals(line[1:])
			if (equal_pos < 0 and mark_pos < 0) or \
			(equal_pos > 0 and mark_pos < 0) :
				if (sharp_pos > 0):
					rules.parse(line.split("#")[0])
				elif (sharp_pos < 0):
					rules.parse(line)
	if (len(rules.goals) == 0):
		print "No Goal"
		sys.exit()
	if (len(rules.data) == 0):
		print "No Rule"
		sys.exit()
	return rules

def look_up(data, goal, visited=None)
	for 




def build_graph(rules):
	for goal in rules.goals:
		look_up(rules.data, goal)
	# build_dps(rules.graph, rules.data)


def main(filename):
	rules = parsing(filename)
	rules.fact = ''.join(set(rules.fact))
	rules.initial_fact = ''.join(set(rules.initial_fact))
	rules.goals = ''.join(set(rules.goals))
	build_graph(rules)

if __name__ == "__main__":
	args = parser.parse_args()
	if (len(args.files) >= 1):
		main(args.files[0])
	else:
		print "Incorrect Argument"

# Si on met un \n directement au debut Parsing Error

