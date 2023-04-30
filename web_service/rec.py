
import numpy as np
import pandas as pd
from prep import FINAL_usergamemat,FINAL_simmat,FINAL_meanmapper
import warnings
warnings.filterwarnings("ignore")

def reco(user_gamename_mat, sim_mat_user, meanmapper, user):
    rem_sim_mat = sim_mat_user.drop(index=user)      
    n = 5 
    simusers = rem_sim_mat[user].sort_values(ascending=False)[:n]

    already_watch = user_gamename_mat[user_gamename_mat.index==user].dropna(axis=1,how='all')
    simi_user_seen = user_gamename_mat[user_gamename_mat.index.isin(simusers.index)].dropna(axis=1,how='all')
    simi_user_seen.drop(already_watch.columns,axis=1,inplace=True,errors="ignore")  
    recom_list = []
    item_score = {}
    for i in simi_user_seen.columns:  
        score = meanmapper.loc[user]["meaner"] 
        movie_rating = simi_user_seen[i]
        for u in simusers.index:
            if pd.isna(movie_rating[u])==False:
                number_of_common_rated = (user_gamename_mat.loc[user].notnull() & user_gamename_mat.loc[u].notnull()).sum()
                if(number_of_common_rated > 5):      
                    number_of_common_rated = 5
                score = score + sim_mat_user.loc[user][u]*movie_rating[u]*number_of_common_rated/abs(sim_mat_user.loc[user][u]*number_of_common_rated) 
        item_score[i] = score

    for i in sorted(item_score.items(), key=lambda x:x[1],reverse=True)[:10]:
        recom_list.append(i[0])
    return recom_list

