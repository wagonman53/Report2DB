import pandas as pd
import bucket
import hand_rank
import community_card
import utils
import db

#データベースの接続設定
database = 'gto'
user = 'postgres'
password = 'eng1969'

paths = utils.get_file_paths()

for folder_name, folder_paths in paths.items():
    df = pd.read_csv(folder_paths["report"], skiprows=3, na_values=["  "])
    df = community_card.get_cc(df)

    oop_hand = pd.read_csv(folder_paths["report_OOP_Full"])
    oop_hand = community_card.get_cc_hand(oop_hand)

    ip_hand = pd.read_csv(folder_paths["report_IP_Full"])
    ip_hand = community_card.get_cc_hand(ip_hand)

    oop_hand = bucket.get_eqrank(oop_hand)
    ip_hand = bucket.get_eqrank(ip_hand,col="IP Equity")

    oop_hand["Hand_rank"] = oop_hand["Community card hand"].map(hand_rank.get_hand_rank)
    ip_hand["Hand_rank"] = ip_hand["Community card hand"].map(hand_rank.get_hand_rank)

    df = bucket.get_bucket(df,oop_hand,ip_hand,"EQ_rank")
    df = bucket.get_bucket(df,oop_hand,ip_hand,"Hand_rank")

    if utils.check_position(oop_hand):
        action_cols = utils.get_action_columns(oop_hand)
        df = bucket.get_bucket_action(df,oop_hand,action_cols,"OOP","EQ_rank")
        df = bucket.get_bucket_action(df,oop_hand,action_cols,"OOP","Hand_rank")
    else:
        action_cols = utils.get_action_columns(ip_hand)
        df = bucket.get_bucket_action(df,ip_hand,action_cols,"IP","EQ_rank")
        df = bucket.get_bucket_action(df,ip_hand,action_cols,"IP","Hand_rank")

    db.save_table(df=df,table_name=folder_name,database=database,user=user,password=password)