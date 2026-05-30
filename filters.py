"""filters.py — Filter logic for the WINDGRID Wind Turbine Dashboard"""
import pandas as pd
import numpy as np


def apply_filters(
    df: pd.DataFrame,
    states: list,
    manufacturers: list,
    year_range: tuple,
    cap_range: tuple,
    hh_range: tuple,
) -> pd.DataFrame:
    out = df.copy()

    if states:
        out = out[out["t_state"].isin(states)]

    if manufacturers:
        out = out[out["t_manu"].isin(manufacturers)]

    if year_range:
        out = out[
            (out["p_year"] >= year_range[0]) &
            (out["p_year"] <= year_range[1])
        ]

    if cap_range:
        valid_cap = out["t_cap"] > 0
        out = out[
            ~valid_cap |
            (
                valid_cap &
                (out["t_cap"] >= cap_range[0]) &
                (out["t_cap"] <= cap_range[1])
            )
        ]

    if hh_range:
        valid_hh = out["t_hh"] > 0
        out = out[
            ~valid_hh |
            (
                valid_hh &
                (out["t_hh"] >= hh_range[0]) &
                (out["t_hh"] <= hh_range[1])
            )
        ]

    return out
