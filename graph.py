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

	def settrack(self,goal):
		paths = self.setpath(goal)
		if (len(paths) == 0):
			return 0
		val = paths.pop()
		self.settrack(val)

	def show(self):
		for key, value in self.graph.iteritems():
			print key, key.value