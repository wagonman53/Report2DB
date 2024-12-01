import pandas as pd


def get_cc(df):
    if "River" in df.columns:
        df = df.dropna(subset=["Flop","Turn","River"]).copy()
        df["Community card"] = df["Flop"] + df["Turn"] + df["River"]
    elif "Turn" in df.columns:
        df = df.dropna(subset=["Flop","Turn"]).copy()
        df["Community card"] = df["Flop"] + df["Turn"]
    else:
        df = df.dropna(subset=["Flop"]).copy()
        df["Community card"] = df["Flop"]
    return df


def get_cc_hand(df):
    if "River" in df.columns:
        df["Community card"] = df["Flop"] + df["Turn"] + df["River"]
        df["Community card hand"] = df["Community card"] + df["Hand"]
    elif "Turn" in df.columns:
        df["Community card"] = df["Flop"] + df["Turn"]
        df["Community card hand"] = df["Community card"] + df["Hand"]
    else:
        df["Community card"] = df["Flop"]
        df["Community card hand"] = df["Community card"] + df["Hand"]
    return df