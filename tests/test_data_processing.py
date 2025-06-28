import pandas as pd
from mylib import data_processing as dp


def test_drop_rows_by_index():
    df = pd.DataFrame(
        {"a": [1, 2, 3, 4, 5],
        "b": [6, 7, 8, 9, 10],
        "c": [11, 12, 13, 14, 15] 
        }
    )
    result = dp.drop_rows_by_index(df, [2, 3])
    expected = pd.DataFrame(
        {"a": [1, 4, 5],
        "b": [6, 9, 10],
        "c": [11, 14, 15] 
        }
    )
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)


def test_drop_rows_by_suffix():
    df = pd.DataFrame(
        {"a": ['a1', 'b2', 'c3', 'd4', 'e5'],
        "b": ['a6', 'prefix7', 'c8', 'd9', 'prefix10'],
        "c": ['a11', 'b12', 'c13', 'd14', 'e15'] 
        }
    )
    result = dp.drop_rows_by_suffix(df, "b", "prefix")
    expected = pd.DataFrame(
        {"a": ['a1', 'c3', 'd4'],
        "b": ['a6', 'c8', 'd9'],
        "c": ['a11', 'c13', 'd14'] 
        }
    )
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)


def test_delete_prefix():
    df = pd.DataFrame(
        {"miasto": ["M.Warszawa", "G.Olsztyn", "M.Kraków", "M-G.Wrocław"]}
    )
    result = dp.delete_prefix(df, 'miasto', ['M.', 'G.', 'M-G.'])
    expected = pd.DataFrame(
        {"miasto": ["Warszawa", "Olsztyn", "Kraków", "Wrocław"]}
    )
    pd.testing.assert_frame_equal(result, expected)


def test_lower_the_case():
    df = pd.DataFrame({"test": ["AAAAAA", "bbBBbb", "cccccC"]})
    result = dp.lower_the_case(df, "test")
    expected = pd.DataFrame({"test": ["aaaaa", "bbbbbb", "cccccc"]})
    pd.testing.assert_frame_equal(result, expected)
