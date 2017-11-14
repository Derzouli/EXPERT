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
def map_tuple_gen(func, tup):
	return tuple(func(itup) for itup in tup)

# decompose chaque term avec la data passee en parametre
def build_term(data):
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
					t = t + Term(s)
				elif (op == '^'):
					t = t + Term(s)
			else:
				t = Term(s)
	return (t)

def build_graph(lst_left, lst_right):
	graph = Graph()
	for key, value in enumerate(lst_left):
		graph.addEdge(value, lst_right[key])
	return graph

def transform(rules):
	trans_list = [map_tuple_gen(build_term, item) for item in rules.data]
	tuple_left, tuple_right = zip(*trans_list)
	lst_left, lst_right = list(tuple_left), list(tuple_right)
	for key, val in enumerate(lst_left):
		try:
			lst_left.append(lst_left[lst_right.index(val)])
			lst_right.append(lst_right[key])
		except ValueError:
			pass
	graph = build_graph(lst_left, lst_right)
	graph.find_path(Term('C'))
