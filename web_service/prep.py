
import warnings

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

import models
from database import engine

warnings.filterwarnings("ignore")
import sqlalchemy as ds
from sqlalchemy.ext.declarative import declarative_base
import pandas
Base = declarative_base()

# DEFINE THE ENGINE (CONNECTION OBJECT)
engines = ds.create_engine("postgresql+psycopg2://postgres:Envious@localhost/envy")


def prep():
    df = pandas.read_sql_query(
        sql=ds.select([models.steams.userid,
                       models.steams.gamename,
                       models.steams.gtype,
                       models.steams.hrs]),
        con=engine
    )

    df.drop_duplicates(keep='last', inplace=True)
    df= df[(df['hrs']>=2) & (df['gtype']=='play')]
    df = df[df.groupby('gamename').userid.transform(len)>=20]

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

    user_gamename_mat = final_df.pivot_table(index="userid",columns="gamename",values="rating")
    meanmapper = user_gamename_mat.copy()
    meanmapper["meaner"] = meanmapper.mean(axis=1)  
    meanmapper = meanmapper[["meaner"]]

    user_gamename_mat = user_gamename_mat.subtract(user_gamename_mat.mean(axis=1),axis=0)
    normed = user_gamename_mat.subtract(user_gamename_mat.mean(axis=1),axis=0)  
    normed = normed.fillna(0) 
    sim_mat_user = cosine_similarity(normed)  
    sim_mat_user = pd.DataFrame(sim_mat_user,columns=normed.index.values,index = normed.index.values) 
    
    return user_gamename_mat, sim_mat_user, meanmapper


FINAL_usergamemat,FINAL_simmat,FINAL_meanmapper = prep()
