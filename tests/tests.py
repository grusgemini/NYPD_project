import pandas as pd
from src.fireevents_and_alcoholsellings_analysis.alcohol_selling_analysis import (
    extract_cities,
    delete_prefix,
    count_how_many,
    separate,
    lowercase_data,
)


def test_extract_cities():
    df = pd.DataFrame(
        {"region": ["M.Warszawa", "gmina Kraków", "M.Poznań", "gmina Gdańsk"]}
    )
    result = extract_cities(df, "region")
    expected = pd.DataFrame({"region": ["M.Warszawa", "M.Poznań"]})
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)


def test_delete_prefix():
    df = pd.DataFrame({"miasto": ["M.Warszawa", "M.Poznań", "gmina Kraków"]})
    result = delete_prefix(df, "miasto", "M.")
    expected = pd.DataFrame({"miasto": ["Warszawa", "Poznań", "gmina Kraków"]})
    pd.testing.assert_frame_equal(result, expected)


def test_count_how_many():
    df = pd.DataFrame(
        {"miasto": ["Warszawa", "warszawa", "WARSZAWA", "Kraków", "kraków"]}
    )
    result = count_how_many(df, "miasto")
    expected = pd.DataFrame({"miasto": ["warszawa", "kraków"], "Count": [3, 2]})
    pd.testing.assert_frame_equal(result, expected)


def test_separate():
    df = pd.DataFrame({"miasta": ["Warszawa, Kraków", "Gdańsk", "Poznań, Wrocław"]})
    result = separate(df, "miasta")
    expected = pd.DataFrame(
        {"miasta": ["Warszawa", "Kraków", "Gdańsk", "Poznań", "Wrocław"]}
    )
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)


def test_lowercase_data():
    df = pd.DataFrame({"miasto": ["WARSZAWA", "Poznań", "Kraków"]})
    result = lowercase_data(df, "miasto")
    expected = pd.DataFrame({"miasto": ["warszawa", "poznań", "kraków"]})
    pd.testing.assert_frame_equal(result, expected)
