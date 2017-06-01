import re

from parsec import string, sepBy, regex, sepEndBy1, spaces, Parser, separated, Value, generate, many1, digit

quoted_string = regex(r'"[^"]*"', re.MULTILINE)
cell = quoted_string ^ regex(r'[^,"\r\n]*')
end_line = regex(r'\r\n?', re.MULTILINE)
row = sepBy(cell, string(",") << spaces())
header = row
csv = (header << end_line) + sepEndBy1(row, end_line)


def parser_by_count(value):
    try:
        num_cells = int(value)
        return separated(cell, string(",") << spaces(), mint=num_cells, maxt=num_cells)
    except ValueError:
        return Parser(lambda index, text: Value.failure(index, "expected a number"))


first_cell = (cell << string(",") << spaces())
counting_parser = first_cell.bind(parser_by_count)


# @generate
def matrix_parser():
    cell = many1(digit()).parsecmap(''.join).parsecmap(int)
    height = yield cell
    yield (string(",") << spaces())
    width = yield cell
    yield string('\n')
    row = separated(cell, string(",") << spaces(), mint=width, maxt=width)
    rows = separated(row, string('\n'), mint=height, maxt=height)
    return rows
