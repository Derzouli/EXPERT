#!/usr/bin/python
import collections
from graph import Graph
import functools

class Term(object):

	def __init__(self, name, value=False):
		self.name = name
		self.value = value

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

# decompose chaque term avec la data passee en parametre
def build_term(data, initial_fact):
	d = collections.deque(data)
	t = 0
	stack_operator = []
	while d:
		s = d.popleft()
		if (s == '+' or s == '^'):
			stack_operator.append(s)
		else:
			if (stack_operator):
				op = stack_operator.pop(0)
				if (op == '+'):
					if s in initial_fact:
						t = t + Term(s, value=True)
					else:
						t = t + Term(s)
				elif (op == '^'):
					if s in initial_fact:
						t = t + Term(s, value=True)
					else:
						t = t + Term(s)
			else:
				if s in initial_fact:
					t = Term(s, value=True)
				else:
					t = Term(s)
	return (t)

def build_graph(lst_left, lst_right):
	graph = Graph()
	for key, value in enumerate(lst_left):
		graph.addEdge(value, lst_right[key])
	return graph

def backtrack(graph, character):
	if (graph.backtrack(Term(character)) == 2):
		graph.settrack(Term(character))

def pathfinding(graph, term):
	path = graph.find_path(term)
	for key, value in enumerate(path):
		if not term.value and len(term) == 1 and \
		value.value:
			graph.update_value(term)
		if len(term) > 1 and value.value:
			for c in term.addition_splitter():
				graph.update(c)

def sub_resolve(graph, character, initial_fact):
	path = graph.find_path(Term(character))
	if len(path) == 0:
		if (character not in initial_fact):
			return False
	for key, value in enumerate(path):
		if not value.value:
			return False
	return True

def resolve(graph, character, initial_fact):
	path = graph.find_path(Term(character))
	result = True
	if len(path) == 0:
		if (character not in initial_fact):
			result = False
	for key, value in enumerate(path):
		if len(value) > 1 and not value.value:
			for c in value.addition_splitter():
				result = result & sub_resolve(graph, c, initial_fact)
	return result

def transform(rules):
	trans_list = [map_tuple_gen(build_term, item, rules.initial_fact) for item in rules.data]
	tuple_left, tuple_right = zip(*trans_list)
	lst_left, lst_right = list(tuple_left), list(tuple_right)
	for key, val in enumerate(lst_left):
		try:
			lst_left.append(lst_left[lst_right.index(val)])
			lst_right.append(lst_right[key])
		except ValueError:
			pass
	graph = build_graph(lst_left, lst_right)
	# print rules.fact
	for character in rules.fact:
		backtrack(graph, character)
	for k, v in enumerate(lst_right):
		pathfinding(graph, v)
	# print resolve(graph, "F", rules.initial_fact)
	print graph.show()
	for character in rules.goals:
		result = graph.lookup(Term(character))
		if not result:
			print character + " is %r " % resolve(graph, character, rules.initial_fact)
		else:
			print character + " is " + " True "
	# path = graph.find_path(Term('M'))
	# print graph.show()
	# print graph.show()
	# for character in rules.
	# path = graph.find_path(Term('K'))
	# solution = True
	# for key, value in enumerate(path):
		# if (value.value is False):
		# 	solution = False
		# print value, value.value
	# print Term('C', value=True).value
