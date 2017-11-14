#!/usr/bin/python
from rules import Rules
import sys

def parsing(filename):
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
	rules.fact = ''.join(set(rules.fact))
	rules.initial_fact = ''.join(set(rules.initial_fact))
	rules.goals = ''.join(set(rules.goals))
	return rules
