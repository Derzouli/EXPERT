#!/usr/bin/python
from collections import defaultdict

class Graph:

	def __init__(self):
		self.graph = defaultdict(list)

	def addEdge(self,u,v):
		self.graph[u].append(v)

	def find_path(self,v):

		visited = []
		for key, value in self.graph.iteritems():
			if (v in value) and (key is not visited):
				visited.append(key)

		return visited

	def backtrack(self,goal):
		paths = self.find_path(goal)
		if (len(paths) == 0):
			return 1
		val = paths.pop()
		if (val.value):
			return 2
		return self.backtrack(val)

	def setpath(self,v):

		visited = []
		for key, value in self.graph.iteritems():
			if (v in value) and (key is not visited):
				visited.append(key)

		for x in visited:
			self.graph[x.setValue(True)]
		return visited

	def settrack(self, goal):
		paths = self.setpath(goal)
		if (len(paths) == 0):
			return 0
		val = paths.pop()
		self.settrack(val)

	# Ici ce n'est pas bon le fait que L soit vrai ne veut pas dire que
	# L + M est vrai, il faut faire un update du terme L + M et donc
	# Ca se fait en deux etapes premierement mettre L a vrai.
	# puis faire un find_path de M / N a vrai.
	# Il faut absolument developper une etape transitoire.
	def update(self, character):
		for key, value in self.graph.iteritems():
			if (character in str(key)):
				self.graph[key.setValue(True)]

	def update_index(self, term):
		for key, value in self.graph.iteritems():
			if key.name == term.name:
				self.graph[key.setValue(True)] 

	def update_value(self, term):
		for key, value in self.graph.iteritems():
			for index, val in enumerate(value):
				if (val.name == term.name):
					value[index] = val.setValue(True)

	def show(self):
		for key, value in self.graph.iteritems():
			print key, key.value, value[0], value[0].value

	def lookup(self, target):
		for key, value in self.graph.iteritems():
			for index, val in enumerate(value):
				if (target.name == val.name):
					return val.value
		return False
