import numpy as np
import pandas as pd
import sqlalchemy
import os


class DBManager:
    def __init__(self, df_name, threshold1=0.55, threshold_mean=0.6):
        self.df_name = df_name
        self.threshold = threshold1
        self.m_threshold = threshold_mean

        print('Loading ' + self.df_name + ' ...', end='')
        creds = open('./db.cred', 'r').read().replace('\n', '')
        self.engine = sqlalchemy.create_engine(f"mariadb+pymysql://{creds}/hauren_mind?charset=utf8mb4", echo=True)
        self.engine.connect()
        self.db_metadata = sqlalchemy.MetaData(bind=self.engine)
        self.engine.execute("USE hauren_mind")
        if True:
            self.df = pd.read_sql_table(df_name, self.engine, index_col='index')
            self.v_columns = ['vec_mean', 'vec1', 'vec2', 'vec3', 'vec4', 'vec5', 'vec6', 'vec7', 'vec8', 'vec9', 'vec10']

            for col in self.v_columns:
                new_vectors = []
                for ind, el in self.df.iterrows():

                    if el[col] == 'None':
                        new_vectors.append('None')
                    else:
                        try:
                            new_vectors.append(np.array(list(map(float, el[col][1: -1].split()))))
                        except Exception as e:
                            pass

                self.df[col] = new_vectors
        else:
            self.df = pd.DataFrame(columns=(['name'] + self.v_columns))

        print('\r' + self.df_name + ' Loaded')

    def find(self, vector):
        for i in range((len(self.df))):
            el = self.df.loc[i]
            if np.linalg.norm(el['vec_mean'] - vector) < self.m_threshold:

                for col in self.v_columns[1:]:
                    if type(el[col]) != str and np.linalg.norm(el[col] - vector) < self.threshold:
                        self.update_vec(i, vector)
                        return el['name']

        return None

    def update_vec(self, ind, val):
        i = 1
        df_mean = self.df.loc[ind]['vec_mean']
        sizes = []
        for el in self.v_columns[1:]:
            if type(self.df.loc[ind][el]) != str:
                i += 1
                sizes.append(np.linalg.norm(self.df.loc[ind][el] - df_mean))
        df_mean *= (i - 1)

        if i < 11:
            df_mean = (df_mean + val) / i
            self.df.loc[ind]['vec' + str(i)] = val
        else:
            i = np.argmax(sizes)
            df_mean += (val - self.df.loc[ind]['vec' + str(i + 1)]) / 10
            self.df.loc[ind]['vec' + str(i + 1)] = val

        self.df.loc[ind]['vec_mean'] = df_mean

    def add(self, name, vector):
        find_name = self.find(vector)
        if find_name is None:
            df_len = len(self.df)
            self.df.loc[df_len] = [name, vector, vector] + ['None'] * (len(self.df.columns) - 3)
            return name
        else:
            return find_name

    def change_name(self, prev, new):
        self.df.loc[self.df['name'] == prev, 'name'] = new
        return new

    def save(self):
        self.df.to_csv(f"./database/{self.df_name}", index=False)
        self.df.to_sql(self.df_name, self.engine, if_exists='replace')
        b = 0