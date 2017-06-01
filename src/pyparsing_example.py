from pyparsing import Regex, OneOrMore, delimitedList, LineEnd, Group

cell = Regex(r'[^",\n\r]+') | Regex(r'"[^"]*"')
row = delimitedList(cell, delim=",") + LineEnd().suppress()
header = row.copy().setName('header')
csv = Group(header) + Group(OneOrMore(Group(row)))
