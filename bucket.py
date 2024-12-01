import pandas as pd
import numpy as np

#EQランクを取得
def get_eqrank(df,col="OOP Equity",range=range(90, -1, -10)):
    def map_rank(x):
        for i in range:
            if x >= i:
                return "EQB" + str(i)
    df["EQ_rank"] = df[col].map(map_rank)
    return df

#バケットを取得
def get_bucket(df,oop_hand,ip_hand,rank_col):
    #ボード毎の合計コンボ数を取得
    oop_total = {}
    ip_total = {}
    for i,g in oop_hand.groupby("Community card"):
        oop_total[i] = g["Weight OOP"].sum()
    for i,g in ip_hand.groupby("Community card"):
        ip_total[i] = g["Weight IP"].sum()
    
    #OOPのEQBを取得
    for e,eg in oop_hand.groupby(rank_col):
        map_dic = {}
        for b,bg in eg.groupby("Community card"):
            map_dic[b] = bg["Weight OOP"].sum() / oop_total[b]
        df["OOP_"+e] = df["Community card"].map(map_dic)
        df["OOP_"+e] = df["OOP_"+e]*100
    
    #IPのEQBを取得
    for e,eg in ip_hand.groupby(rank_col):
        map_dic = {}
        for b,bg in eg.groupby("Community card"):
            map_dic[b] = bg["Weight IP"].sum() / ip_total[b]
        df["IP_"+e] = df["Community card"].map(map_dic)
        df["IP_"+e] = df["IP_"+e]*100
    
    return df

#バケット毎のアクション頻度を取得
def get_bucket_action(df, hand_df, action_col, position, rank_col):
    all_results = {}
    
    for a in action_col:
        hand_df[a + "_weight"] = (hand_df[a] / 100) * hand_df["Weight " + position]
        
        for r, rg in hand_df.groupby(rank_col):
            pivot_data = rg.groupby("Community card").agg({
                a + "_weight": "sum",
                "Weight " + position: "sum"
            }).reset_index()
            
            pivot_data["result"] = np.where(
                pivot_data["Weight " + position] > 0,
                pivot_data[a + "_weight"] / pivot_data["Weight " + position] * 100,
                0
            )
            
            map_dic = dict(zip(pivot_data["Community card"], pivot_data["result"]))
            
            col_name = r + a
            all_results[col_name] = df["Community card"].map(map_dic)
    
    result_df = pd.concat([df, pd.DataFrame(all_results)], axis=1)
    
    return result_df