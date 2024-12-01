from collections import Counter

card_num = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3,
                '2': 2, "1": 1}

#ストレート判定関数
def has_straight(lst):
    unique_sorted = sorted(set(lst))

    if len(unique_sorted) < 5:
        return False

    if set(unique_sorted).issubset([14,2,3,4,5]):
        return True

    counter = 1
    for i in range(1, len(unique_sorted)):
        if unique_sorted[i] == unique_sorted[i - 1] + 1:
            counter += 1
            if counter >= 5:
                return True
        else:
            counter = 1
    return False


def get_hand_rank(h):
    x = list(h.replace(" ", ""))

    if len(x) == 10:
        n = [card_num[x[0]], card_num[x[2]], card_num[x[4]], card_num[x[6]], card_num[x[8]]]
        tn = n[:3]
        s = [x[1], x[3], x[5], x[7], x[9]]
    elif len(x) == 12:
        n = [card_num[x[0]], card_num[x[2]], card_num[x[4]], card_num[x[6]], card_num[x[8]], card_num[x[10]]]
        tn = n[:4]
        s = [x[1], x[3], x[5], x[7], x[9], x[11]]
    elif len(x) == 14:
        n = [card_num[x[0]], card_num[x[2]], card_num[x[4]], card_num[x[6]], card_num[x[8]], card_num[x[10]], card_num[x[12]]]
        tn = n[:5]
        s = [x[1], x[3], x[5], x[7], x[9], x[11], x[13]]
    else:
        return

    pn = n[-2:]
    nc = Counter(n).most_common()
    tc = Counter(tn).most_common()
    sc = Counter(s).most_common()
    tm = sorted(list(set(tn)))
    tm.sort(reverse=True)

    #ストレートフラッシュの判定
    if sc[0][1] >= 5:
        if has_straight(n):
            return "straight flush"
    #4カードの判定
    if nc[0][1] == 4:
        return "4 Cards"
    #フルハウスの判定
    if (nc[0][1] == 3) and (nc[1][1] > 1):
        return "full house"
    #フラッシュの判定
    if sc[0][1] >= 5:
        return "flush"
    #ストレートの判定
    if has_straight(n):
        return "straight"
    #3カードの判定
    if nc[0][1] == 3:
        return "3 Cards"
    #2ペアの判定
    if (nc[0][1] == 2 and nc[1][1] == 2) and (tc[0][1]==1):
        return "2 pairs"
    #オーバーペアの判定
    if (pn[0] == pn[1]) and (pn[0] > max(tn)):
        return "over pair"
    #トップペアの判定
    if max(tn) in pn:
        if pn[0] in tn:
            if pn[1] in [14,13,12,11]:
                return "top pair(GK)"
        if pn[1] in tn:
            if pn[0] in [14,13,12,11]:
                return "top pair(GK)"
        return "top pair(LK)"
    #ミドルペアの判定
    if len(tm) > 1:
        if tm[1] in pn:
            return "middle pair"
        if (pn[1] == pn[0]) and (pn[1] >= tm[1]):
            return "middle pair"
    #ボトムペアの判定
    if (pn[0] in tn) or (pn[1] in tn):
        return "low pair"
    if pn[1] == pn[0]:
        return "low pair"
    return "noting"