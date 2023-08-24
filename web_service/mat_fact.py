
import numpy as np
import pandas as pd
from preper import prepy
import pickle
from sklearn.ensemble import RandomForestRegressor
import warnings
warnings.filterwarnings("ignore")

def updater():
    matrix_factoriza()

def matrix_factoriza(K=10, steps=30, alpha=0.01, beta=0.01):
    train, test, user_le, game_le = prepy()

    util_df = pd.pivot_table(data=train, values='rating', index='userid', columns='gamename')
    util_df.fillna(0, inplace=True)

    R = np.array(util_df)
    P = np.random.rand(len(R), K)
    Q = np.random.rand(len(R[0]), K).T

    for step in range(steps):
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:
                    eij = R[i][j] - np.dot(P[i, :], Q[:, j])  # calculate error

                    for k in range(K):
                        # calculate gradient with alpha and beta parameter
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])

        e = 0
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:
                    e = e + pow(R[i][j] - np.dot(P[i, :], Q[:, j]), 2)

        rmse = np.sqrt(e / len(R[R > 0]))
        # print('step :', step+1, 'RMSE :', rmse)
        if rmse < 0.01:
            break
    f = open('another.pckl', 'wb')
    f.seek(0)
    f.truncate()
    pickle.dump([train,test,util_df,user_le, game_le,P,Q.T], f)
    f.close()
   # return P, Q.T, util_df


def recommend(user_id, n=10):
    f = open('another.pckl', 'rb')
    train,test,util_df,user_le, game_le,nP,nQ= pickle.load(f)
    nR = np.dot(nP, nQ.T)

    f.close()
    user_ind = user_le.transform(np.array([user_id]))[0]
    user_idx = np.where(util_df.index == user_ind)[0][0]

    unrated_gamename = util_df.loc[user_ind][util_df.loc[user_ind] == 0].index

    unrated_gamename_df = pd.DataFrame()
    unrated_gamename_df['gamename'] = game_le.inverse_transform(unrated_gamename)
    unrated_gamename_df['rating'] = nR[user_idx][unrated_gamename]
    unrated_gamename_df = unrated_gamename_df.sort_values(by='rating', ascending=False).reset_index(drop=True)

    unrated_gamename_df['rating'] = unrated_gamename_df['rating'].apply(lambda x: round(x))
    unrated_gamename_df['rating'] = unrated_gamename_df['rating'].apply(lambda x: 5 if x > 5 else x)
    unrated_gamename_df['rating'] = unrated_gamename_df['rating'].apply(lambda x: 1 if x < 1 else x)
    new_reco = []
    for i in unrated_gamename_df['gamename'][:10]:
        new_reco.append(i)
    return new_reco


def LTR( userid):
    f = open('another.pckl', 'rb')
    train, test, util_df, user_le, game_le, nP, nQ = pickle.load(f)

    f.close()
    user_ind = user_le.transform(np.array([userid]))[0]
    user_df = train[train['userid']==user_ind]

    x_train = nQ[user_df['gamename']][:]
    y_train = user_df['rating']
    x_test = nQ[test['gamename']][:]

    rf = RandomForestRegressor(n_estimators=500, max_depth=6, min_samples_leaf=8, n_jobs=-1)
    rf.fit(x_train, y_train)

    # show the top 10 games with highest predicted rating
    pred_df = pd.DataFrame()
    pred_df['gamename'] = game_le.inverse_transform(test['gamename'])
    pred_df['rating'] = rf.predict(x_test)
    pred_df = pred_df.sort_values(by='rating', ascending=False).reset_index(drop=True)

    pred_df['rating'] = pred_df['rating'].apply(lambda x:round(x))
    pred_df['rating'] = pred_df['rating'].apply(lambda x:5 if x>5 else x)
    pred_df['rating'] = pred_df['rating'].apply(lambda x:1 if x<1 else x)
    pred_df.drop_duplicates(subset=['gamename'], inplace=True, keep='first')
    newer = []
    for i in pred_df['gamename'][:10]:
        newer.append(i)
    return newer