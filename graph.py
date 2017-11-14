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

	def show(self):
		for key, value in self.graph.iteritems():
			print key, value