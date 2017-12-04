#!/usr/bin/python
import collections
from graph import Graph
import functools
import sys
from sets import Set

class Term(object):

	def __init__(self, name, value=False):
		self.name = name
		self.value = value
		self.or_value = False

	def setOrValue(self):
		self.or_value = True  # If its for OR operator
		return self

	def getName(self):
		return self.name

	def setValue(self, value):
		self.value = value
		return self

	def addition_splitter(self):
		return set(self.name.split("+"))

	def getValue(self):
		return self.value

	def __len__(self):
		return len(self.name)

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

# applique sur chaque element du tuple la fonction de decomposition de term
def map_tuple_gen(func, tup, initial_fact):
	return tuple(func(itup, initial_fact) for itup in tup)

def error_parenthese():
	print "PARENTHESES ARE NOT WORKING"
	sys.exit(1)
# decompose chaque term avec la data passee en parametre
def build_term(data, initial_fact):
	d = collections.deque(data)
	t = 0
	stack_operator = []
	invert_operator = []
	while d:
		s = d.popleft()
		if (s == '!'):
			invert_operator.append(s)
		elif (s == '+' or s == '^'):
			stack_operator.append(s)
		else:
			if (stack_operator):
				op = stack_operator.pop(0)			
				if (op == '+'):
					if (invert_operator):
						invert_operator.pop(0)
						if type(s) is list:
							error_parenthese()
						if s in initial_fact:
							t = t + ~Term(s, value=True)
						else:
							t = t + ~Term(s)
					else:
						if type(s) is list:
							error_parenthese()
						if s in initial_fact:
							t = t + Term(s, value=True)
						else:
							t = t + Term(s)
				elif (op == '^'):
					if (invert_operator):
						invert_operator.pop(0)
						if type(s) is list:
							error_parenthese()
						if s in initial_fact:
							t = t ^ ~Term(s, value=True)
						else:
							t = t ^ ~Term(s)
					else:
						if type(s) is list:
							error_parenthese()
						if s in initial_fact:
							t = t ^ Term(s, value=True)
						else:
							t = t ^ Term(s)
			else:
				if type(s) is list:
					error_parenthese()
				if s in initial_fact:
					t = Term(s, value=True)
				else:
					t = Term(s)
				if (invert_operator):
					invert_operator.pop(0)
					t = ~t
	return (t)

def build_graph(lst_left, lst_right):
	graph = Graph()
	for key, value in enumerate(lst_left):
		graph.addEdge(value, lst_right[key])
	return graph

def backtrack(graph, character):
	if (graph.backtrack(Term(character)) == 2):
		graph.settrack(Term(character))

def pathfinding(graph, term, initial_fact):
	path = graph.find_path(term)
	for key, value in enumerate(path):
		if not term.value and len(term) == 1 and \
		value.value:
			graph.update_value(term)
		if len(term) > 1 and value.value:
			for c in term.addition_splitter():
				graph.update(c)
		if len(value) > 1 and not value.value:
			result = True
			for c in value.addition_splitter():
				result = result & sub_resolve(graph, c, initial_fact)
			if result:
				graph.update_value(term)

def sub_resolve(graph, character, initial_fact):
	path = graph.find_path(Term(character))
	if len(path) == 0:
		if (character not in initial_fact):
			return False
	for key, value in enumerate(path):
		if not value.value:
			return False
	return True

def resolve(graph, character):
	path = graph.find_path(Term(character))
	for key, value in enumerate(path):
		if value.value:
			graph.update_value(Term(character))

def group(seq, sep):
	g = []
	for el in seq:
		if el == sep:
			yield g
			g = []
		else:
			g.append(el)
	yield g

def filter_or_operator(data):
	combs = []
	for k, v in data:
		if '|' in k:
			result = list(group(k, '|'))
			for key, value in enumerate(result):
				combs.append((value, v))
		else:
			combs.append((k, v))
	return combs

def checker(c, graph):
	for key, value in graph.graph.iteritems():
		for k, v in enumerate(value):
			if v.value and c == v.name:
				return True
	return False

def reconstruct(graph):
	for key, value in graph.graph.iteritems():
		if len(key) > 1 and not key.value:
			stack_operator = []
			t = 0
			for c in key.name:
				if c == '+' or c == '^':
					stack_operator.append(c)
				else:
					if (stack_operator):
						op = stack_operator.pop(0)
						if (op == '+'):
							t = t + Term(c, value=checker(c, graph))
						elif (op == '^'):
							t = t ^ Term(c, value=checker(c, graph))
					else:
						t = Term(c, value=checker(c, graph))
			if t.value:
				graph.update_index(t)

def naming(a):
	return a.name

def check_verify(lst_left, lst_right):
	s = set()
	left = list(map(naming, lst_left))
	right = list(map(naming, lst_right))
	lis = [(x,y) for (x,y) in zip(left, right) if x != y]
	if len(lis) != len(left):
		print "INCORRECT RULES CASE: INCORRECT EQUALITY OF FACT"
		sys.exit(1)
	seen = dict()
	for i in lis:
		if tuple((i[1], i[0])) in s:
			print "INCORRECT RULES CASE"
			sys.exit(1)
		s.add((i[0], i[1]))

def transform(rules):
	rules.data = filter_or_operator(rules.data)
	trans_list = [map_tuple_gen(build_term, item, rules.initial_fact) for item in rules.data]
	tuple_left, tuple_right = zip(*trans_list)
	lst_left, lst_right = list(tuple_left), list(tuple_right)
	check_verify(lst_left, lst_right)
	for key, val in enumerate(lst_left):
		try:
			lst_left.append(lst_left[lst_right.index(val)])
			lst_right.append(lst_right[key])
		except ValueError:
			pass
	graph = build_graph(lst_left, lst_right)
	for character in rules.fact:
		backtrack(graph, character)
	for k, v in enumerate(lst_right):
		pathfinding(graph, v, rules.initial_fact)
	reconstruct(graph)
	for k, v in enumerate(rules.goals):
		resolve(graph,v)
	print graph.show()
	for character in rules.goals:
		if character in rules.initial_fact:
			print character + " is " + "True"
		else:
			result = graph.lookup(Term(character))
			print character + " is %r " % result
