#!/usr/bin/python

from pyparsing import Group, Literal, Optional, Regex, Word, ZeroOrMore, Upcase, alphas
from collections import Counter
from pyparsing import ParseException

# 1 PLUS
# 2 NOT
# 3 OR
# 4 XOR

def grammar():
	_and = Literal('+').setParseAction(lambda:'+')
	_not = Literal('!').setParseAction(lambda:'!')
	_or =  Literal('|').setParseAction(lambda:'|')
	_xor =  Literal('^').setParseAction(lambda:'^')
	sign = _and | _not | _or | _xor
	letter = Word(alphas, exact=1)
	atom = letter | Optional(_not) + letter('not')
	monomial = Optional(sign('sign')) + atom
	polynomial = Group(monomial) + ZeroOrMore(monomial)
	return polynomial('left') + '=>' + polynomial('right')


_grammar = grammar()

def parse(s):
	try:
		equation = _grammar.parseString(s)
	except ParseException:
		print "NIQUE TA MERE"
		return (-1);
	series = Counter()
	print equation
	# for side, terms in ((+1, equation.left), (-1, equation.right)):
	# 	for t in terms:
	# 		n = side * t.get('joiner', 1) * t.get('sign', 1) * t.get('coeff', 1)
	# 		series[t.get('exponent', 0)] += n
	# try:
	# 	degree = max(e for e, c in series.items() if c)
	# except ValueError as e:
	# 	print("Every numbers belongs to the set of real numbers are solutions")
	# 	return 0
	# return [series[e] for e in range(degree, -1, -1)]


if __name__ == "__main__":
	parse("AC | B => C")