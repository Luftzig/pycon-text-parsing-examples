import pyparsing
import pytest

import pyparsing_example as p
from pyparsing_example import csv


def test_cell():
    x = 'bla'
    assert p.cell.parseString(x)[0] == x


def test_cell_with_quotes():
    x = '"bla,\n"'
    assert p.cell.parseString(x)[0] == x


def test_reject_cell_comma():
    x = 'bla,'
    with pytest.raises(pyparsing.ParseException):
        p.cell.parseString(x, parseAll=True)


def test_row():
    in_string = 'ab, ba\r\n'
    assert p.row.parseString(in_string).asList() == ['ab', 'ba']


def test_simple():
    in_string = 'col1,col2\r\nval1,val2\r\n'
    result = csv.parseString(in_string)
    assert result[0].asList() == ['col1', 'col2']
    assert result[1][0].asList() == ['val1', 'val2']


def test_single_line():
    in_string = 'header, cell1\r\nvalue, "quoted\r\n value"'
    result = csv.parseString(in_string)
    assert result[1][0].asList() == ["value", '"quoted\r\n value"']


def test_multi_line():
    in_string = "a,b\r\n1,4\r\n5,6"
    result = csv.parseString(in_string)
    assert result[1].asList() == [["1", "4"], ["5", "6"]]
