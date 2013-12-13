#! /usr/bin/env python

#  $ ./foo.py
#  BEFORE: A \\" \\\" Z
#  AFTER : A \\ \\\" Z
#  
#  BEFORE: A \\\" \\" Z
#  AFTER : A \\\" \\ Z

from re import compile as Regex

def remove_first_group(m):
	start = m.start(1) - m.start(0)
	end = m.end(1) - m.start(0)
	whole_match = m.group(0)

	return whole_match[:start] + whole_match[end:]

unescaped_doublequote = Regex(r'(?<!\\)(?:\\\\)*(")')

for test in (
		r'A \\" \\\" Z',
		r'A \\\" \\" Z',
):
	print 'BEFORE:', test
	print 'AFTER :', unescaped_doublequote.sub(remove_first_group, test)
	print


