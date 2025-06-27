import pandas as pd
import numpy as np 
import sys

def statistics(data: pd.DataFrame, column: str):
    """Calculates basic statistics such as count, mean, standard deviation, minimum, maximum and median.
    :param data: Input DataFrame
    :param column: Name of the column where the statistics are to be calculated
    """
    if column not in data.columns:
        raise ValueError(f"Column {column} not found in DataFrame.")

    series = pd.to_numeric(data[column], errors="coerce").dropna()

    stats = {
        "count": int(series.count()),
        "mean": round(series.mean().item(), 2),
        "std": round(series.std().item(), 2),
        "min": int(series.min().item()),
        "max": int(series.max().item()),
        "median": int(series.median()) # round to integer in case of .5
    }

    return stats



