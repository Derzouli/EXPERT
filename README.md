#Expert System
for more information: https://en.wikipedia.org/wiki/Expert_system \
Implementation of  backward-chaining inference engine. \
Rules and facts will be given as a text file named test_XX, \
A fact can be any uppercase alphabetical character. \
To execute the program run ./expert.py test_XX \
Only input file is accepted \
The file contains a list of rules, then a list of initial facts, then a list of queries. \
The program must, given the facts and rules given, tell if the query is true, false or undetermined \
By default, all facts are false, and can only be made true by the initial facts statement, or by application of a rule. \
A fact can only be undetermined if the ruleset is ambiguous, for example if I say "A is true, also if A then B or C", then B and C are undetermined. \
If there is an error in the input, for example a contradiction in the facts, or a syntax error, the program inform the user of the problem. \

Here’s a list of the features the engine support. \
• "AND" conditions. For example, "If A and B and [...] then X" \
• "OR" conditions. For example, "If C or D then Z" \
• "XOR" conditions. For example, "If A xor E then V". Remember that this \
means "exclusive OR". It is only true if one and only one of the operands is true. \
• Negation. For example, "If A and not B then Y" \
• Multiple rules can have the same fact as a conclusion \
• "AND" in conclusions. For example, "If A then B and C" \

This repository is only for educational purpose. \
Commits are not correctly named. \
