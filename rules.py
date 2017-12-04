#!/usr/bin/python
from pyparsing import ParseException
from pyparsing import Group, Literal, Optional, Regex, Word, ZeroOrMore, Upcase, alphas, Forward
from pyparsing import ParseException
import sys

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