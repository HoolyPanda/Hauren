import sqlalchemy
import pymysql
import csv
import pandas
from df_manager import DBManager
pymysql.install_as_MySQLdb()
creds = open('./db.cred', 'r').read().replace('\n', '')
engine = sqlalchemy.create_engine(f"mariadb+pymysql://{creds}/hauren_mind?charset=utf8mb4", echo=True)
engine.connect()
engine.execute("USE hauren_mind")
# engine.execute("CREATE DATABASE hauren_mind") #create db
a = sqlalchemy.inspect(engine)
a = a.get_schema_names()
# b = engine.metafdata.tables.keys()
inspector = sqlalchemy.inspect(engine)

for table_name in inspector.get_table_names():
    for column in inspector.get_columns(table_name):
        print("Column: %s" % column['name'])

# def export_vectors():
#                 # self.df = pd.read_csv(df_name)
#     self.df = pd.read_sql_table(df_name, self.engine, index_col='index')
#     # a= list(self.df.columns)
#     # ['name', 'vec_mean', 'vec1', 'vec2', 'vec3', 'vec4', 'vec5', 'vec6', 'vec7', 'vec8', 'vec9', 'vec10']
#     self.v_columns = ['vec_mean', 'vec1', 'vec2', 'vec3', 'vec4', 'vec5', 'vec6', 'vec7', 'vec8', 'vec9', 'vec10']

#     for col in self.v_columns:
#         new_vectors = []
#         for ind, el in self.df.iterrows():

#             if el[col] == 'None':
#                 new_vectors.append('None')
#             else:
#                 try:
#                     new_vectors.append(np.array(list(map(float, el[col][1: -1].split()))))
#                 except Exception as e:
#                     pass

#         self.df[col] = new_vectors
#         # else:
#         #     self.df = pd.DataFrame(columns=(['name'] + self.v_columns))

masters = 'database/masters.csv'
pioners = 'database/pioners.csv'
a = pandas.read_csv(masters)
a.to_sql("masters", engine, if_exists='replace')
a = pandas.read_csv(pioners)
a.to_sql("pioners", engine, if_exists='replace')
# m = pandas.read_sql_table('masters', engine)
# m_df = DBManager("masters")
# m_df.to_sql("masters", engine, if_exists='replace')
# p_df = DBManager("pioners")
# m_df.save()
# n = 0
