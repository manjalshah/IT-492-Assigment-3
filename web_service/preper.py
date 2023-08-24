
import numpy as np
import pandas as pd
from database import engine

import sqlalchemy as ds
from sqlalchemy.ext.declarative import declarative_base
from sklearn import preprocessing
import warnings
warnings.filterwarnings("ignore")

Base = declarative_base()
# DEFINE THE ENGINE (CONNECTION OBJECT)
engines = ds.create_engine("postgresql+psycopg2://postgres:mms10503@localhost/postgres")



def prepy():

    df = pd.read_sql_table('steams', engines)
    df.drop_duplicates(keep='last', inplace=True)
    
    df= df[(df['hrs']>=2) & (df['gtype']=='play')]
    df = df[df.groupby('gamename').userid.transform(len)>=10]

    average = df.groupby(['gamename'],as_index = False).hrs.mean()
    average.rename(columns = {'hrs':'avg_hrs'}, inplace = True)
    df = df.merge(average,on = 'gamename')

    condition = [
                    df['hrs']>= (0.8*df['avg_hrs']),
                    (df['hrs']>=0.6*df['avg_hrs'])&(df['hrs']<0.8*df['avg_hrs']),
                    (df['hrs']>=0.4*df['avg_hrs'])&(df['hrs']<0.6*df['avg_hrs']),
                    (df['hrs']>=0.2*df['avg_hrs'])&(df['hrs']<0.4*df['avg_hrs']),
                    df['hrs']>=0
                ]

    values = [5,4,3,2,1]
    df['rating'] = np.select(condition,values)
    final_df = df[['userid', 'gamename', 'rating']]

    user_le = preprocessing.LabelEncoder()
    user_le.fit(final_df['userid'])
    final_df['userid'] = user_le.transform(final_df['userid'])
    game_le = preprocessing.LabelEncoder()
    game_le.fit(final_df['gamename'])
    final_df['gamename'] = game_le.transform(final_df['gamename'])

    train_ind = []
    test_ind = []

    np.random.seed(0)
    for user_id in final_df['userid'].unique():
        examples = list(final_df[final_df['userid'] == user_id].index)
        np.random.shuffle(examples)

        if(len(examples)>5):
            # store 80% of the examples in train and the rest in test
            train_ind += examples[ : int(0.8*len(examples))]
            test_ind += examples[int(0.8*len(examples)) : ]

    train = final_df.loc[train_ind, :].reset_index(drop=True)
    test = final_df.loc[test_ind, :].reset_index(drop=True)
    print(train.head(50))

    return train, test, user_le, game_le