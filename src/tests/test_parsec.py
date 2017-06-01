import parsec
import pytest

import parsec_example as p
from parsec_example import csv


def test_cell():
    x = 'bla'
    assert p.cell.parse(x) == 'bla'


def test_cell_with_quotes():
    x = '"bla,\n"'
    assert p.cell.parse(x) == x


def test_reject_cell_comma():
    x = 'bla,'
    with pytest.raises(parsec.ParseError):
        p.cell.parse_strict(x)


def test_row():
    in_string = 'ab, ba\r\n'
    assert p.row.parse(in_string) == ['ab', 'ba']


def test_simple():
    in_string = 'col1,col2\r\nval1,val2'
    result = csv.parse(in_string)
    assert result[0] == ['col1', 'col2']
    assert result[1] == [['val1', 'val2']]


def test_single_line():
    in_string = 'header, cell1\r\nvalue, "quoted\r\n value"'
    result = csv.parse(in_string)
    assert result[1] == [["value", '"quoted\r\n value"']]


def test_multi_line():
    in_string = "a,b\r\n1,4\r\n5,6"
    result = csv.parse(in_string)
    assert result[1] == [["1", "4"], ["5", "6"]]


def test_parse_by_count_valid():
    in_string = '2, hello, world'
    result = p.counting_parser.parse(in_string)
    assert result == ['hello', 'world']


def test_parse_by_count_too_few():
    in_string = '3, hello, world'
    with pytest.raises(parsec.ParseError):
        p.counting_parser.parse(in_string)


def test_parse_by_count_too_many():
    in_string = '2, hello, python, world'
    with pytest.raises(parsec.ParseError):
        p.counting_parser.parse_strict(in_string)


def test_parse_not_a_number():
    in_string = 'bla, not, parsing, this'
    with pytest.raises(parsec.ParseError):
        p.counting_parser.parse(in_string)


def test_matrix_1x1():
    in_string = '1,1\n42'
    result = p.matrix_parser.parse(in_string)
    assert result == [[42]]


def test_matrix_2x3():
    in_string = '2,3\n42, 11, 33\n6, 5, 100'
    result = p.matrix_parser.parse(in_string)
    assert result == [
        [42, 11, 33],
        [6, 5, 100]
    ]
