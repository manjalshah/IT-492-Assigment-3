
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from preper import prepy
import warnings
warnings.filterwarnings("ignore")


def helper():
    train, test, user_le, game_le = prepy()
    user_gamename_mat = train.pivot_table(index="userid", columns="gamename", values="rating")

    meanmapper = user_gamename_mat.copy()
    meanmapper["meaner"] = meanmapper.mean(axis=1)
    meanmapper = meanmapper[["meaner"]]

    user_gamename_mat = user_gamename_mat.subtract(user_gamename_mat.mean(axis=1), axis=0)
    normed = user_gamename_mat.subtract(user_gamename_mat.mean(axis=1), axis=0)
    normed = normed.fillna(0)
    sim_mat_user = cosine_similarity(normed)
    sim_mat_user = pd.DataFrame(sim_mat_user, columns=normed.index.values, index=normed.index.values)

    return user_gamename_mat, meanmapper, sim_mat_user,user_le,game_le


def reco( userid,k=5, n=10):
    user_gamename_mat, meanmapper, sim_mat_user, user_le, game_le = helper()
    user = user_le.transform([userid])[0]
    rem_sim_mat = sim_mat_user.drop(index=user)
    simusers = rem_sim_mat[user].sort_values(ascending=False)[:k]
    # print(simusers)

    already_watch = user_gamename_mat[user_gamename_mat.index == user].dropna(axis=1, how='all')
    # print(already_watch)
    simi_user_seen = user_gamename_mat[user_gamename_mat.index.isin(simusers.index)].dropna(axis=1, how='all')
    simi_user_seen.drop(already_watch.columns, axis=1, inplace=True, errors="ignore")
    # print(simi_user_seen)

    pred_df = pd.DataFrame(columns=["gamename", "rating"])
    for i in simi_user_seen.columns:
        score = meanmapper.loc[user]["meaner"]

        movie_rating = simi_user_seen[i]
        for u in simusers.index:
            if pd.isna(movie_rating[u]) == False:
                number_of_common_rated = (
                            user_gamename_mat.loc[user].notnull() & user_gamename_mat.loc[u].notnull()).sum()
                if (number_of_common_rated > k):
                    number_of_common_rated = k
                if (sim_mat_user.loc[user][u] * number_of_common_rated > 0):
                    score = score + sim_mat_user.loc[user][u] * movie_rating[u] * number_of_common_rated / abs(
                        sim_mat_user.loc[user][u] * number_of_common_rated)

        if (score > 5):
            score = 5
        elif (score < 1):
            score = 1

        # add to pred_df using loc
        pred_df.loc[len(pred_df)] = [game_le.inverse_transform(np.array([i]))[0], score]


    pred_df = pred_df.sort_values(by='rating', ascending=False).reset_index(drop=True)
    pred_df['rating'] = pred_df['rating'].apply(lambda x: round(x))
    reco = []
    for i in pred_df["gamename"][:n]:
        reco.append(i)
    return reco