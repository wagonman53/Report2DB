import pandas as pd
import collections

card_num = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}
card_num2 = {'A': 1, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}


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


def high_num(x):
    if x:
        x = list(x.replace(" ", ""))
        cn = [card_num[x[0]], card_num[x[2]], card_num[x[4]]]
        return max(cn)


def middle_num(x):
    if x:
        x = list(x.replace(" ", ""))
        cn = [card_num[x[0]], card_num[x[2]], card_num[x[4]]]
        cns = sorted(cn, reverse=True)
        return cns[1]


def bottom_num(x):
    if x:
        x = list(x.replace(" ", ""))
        cn = [card_num[x[0]], card_num[x[2]], card_num[x[4]]]
        cns = sorted(cn, reverse=True)
        return cns[2]


def turn_num(x):
    x = list(x.replace(" ", ""))
    if len(x)>6:
        return card_num[x[6]]


def river_num(x):
    x = list(x.replace(" ", ""))
    if len(x)>8:
        return card_num[x[8]]


def flop_suit_num(x):
    x = list(x.replace(" ", ""))
    s = [x[1], x[3], x[5]]
    sc = collections.Counter(s).most_common()
    
    return sc[0][1]


def turn_suit_num(x):
    x = list(x.replace(" ", ""))
    if len(x) < 8:
        return
    s = [x[1], x[3], x[5], x[7]]
    sc = collections.Counter(s).most_common()
    
    return sc[0][1]


def river_suit_num(x):
    x = list(x.replace(" ", ""))
    if len(x) < 10:
        return
    s = [x[1], x[3], x[5], x[7], x[9]]
    sc = collections.Counter(s).most_common()
    
    return sc[0][1]


def turn_fc(x):
    t = list(x.replace(" ", ""))
    if len(t) < 8:
        return
    fs = [t[1], t[3], t[5]]
    ts = t[7]
    sc = collections.Counter(fs).most_common()

    if (sc[0][1]==2) and (sc[0][0] == ts):
        return 1
    return 0


def river_fc(x):
    r = list(x.replace(" ", ""))
    if len(r) != 10:
        return
    ts = [r[1], r[3], r[5], r[7]]
    rs = r[9]
    sc = collections.Counter(ts).most_common()
    
    if (sc[0][1]==2) and (sc[0][0] == rs):
        return 1
    return 0


def pair_num(x):
    x = list(x.replace(" ", ""))
    n = [card_num[x[0]], card_num[x[2]], card_num[x[4]]]
    nc = collections.Counter(n).most_common()
    
    if nc[0][1] >= 2:
        return nc[0][0]
    return 0


def turn_paired(x):
    t = list(x.replace(" ", ""))
    if len(t) < 8:
        return
    fn = [card_num[t[0]], card_num[t[2]], card_num[t[4]]]
    tn =  card_num[t[6]]

    if tn in fn:
        return 1
    return 0


def river_paired(x):
    r = list(x.replace(" ", ""))
    if len(r) != 10:
        return
    tn = [card_num[r[0]], card_num[r[2]], card_num[r[4]], card_num[r[6]]]
    rn =  card_num[r[8]]
    
    if rn in tn:
        return 1
    return 0


def flop_connect(x):
    x = list(x.replace(" ", ""))
    n = [card_num[x[0]], card_num[x[2]], card_num[x[4]]]
    n_set = set(n)
    ns = sorted(list(set(n)))
    st = [14,2,3,4,5]

    if len(ns) == 3:
        if ns[2]-ns[0]<=4:
            return 1
    if len(n_set.intersection(set(st))) >= 3:
        return 1
    return 0


def turn_connect(x):
    x = list(x.replace(" ", ""))
    n = [card_num[x[0]], card_num[x[2]], card_num[x[4]], card_num[x[6]]]
    n_set = set(n)
    ns = sorted(list(set(n)))
    st = [14,2,3,4,5]

    if len(ns) == 4:
        if (ns[3]-ns[1]<=4) or (ns[2]-ns[0]<=4):
            return 1
    if len(ns) == 3:
        if ns[2]-ns[0]<=4:
            return 1
    if len(n_set.intersection(set(st))) >= 3:
        return 1
    return 0


def river_connect(x):
    x = list(x.replace(" ", ""))
    n = [card_num[x[0]], card_num[x[2]], card_num[x[4]], card_num[x[6]], card_num[x[8]]]
    n_set = set(n)
    ns = sorted(list(set(n)))
    st = [14,2,3,4,5]

    if len(ns) == 5:
        if (ns[4]-ns[2]<=4) or (ns[3]-ns[1]<=4) or (ns[2]-ns[0]<=4):
            return 1
    if len(ns) == 4:
        if (ns[3]-ns[1]<=4) or (ns[2]-ns[0]<=4):
            return 1
    if len(ns) == 3:
        if ns[2]-ns[0]<=4:
            return 1
    if len(n_set.intersection(set(st))) >= 3:
        return 1
    return 0