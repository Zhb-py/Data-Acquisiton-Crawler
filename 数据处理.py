import pandas as pd
import os

# 1. 用户数据清洗
# (1) 读取数据
users_df = pd.read_csv('data/users.dat', sep='::', header=None, engine='python')
users_df.columns = ['userID', 'gender', 'age', 'occupation', 'zip-code']

# (2) 用众数填充缺失值
users_df['gender'].fillna(users_df['gender'].mode()[0], inplace=True)

# (3) 保存到clean_data目录
if not os.path.exists('Desktop/大数据应用与服务实训项目/数据采集与处理/任务二 电影数据处理/film/clean_data'):
    os.makedirs('Desktop/大数据应用与服务实训项目/数据采集与处理/任务二 电影数据处理/film/clean_data')
users_df.to_csv('Desktop/大数据应用与服务实训项目/数据采集与处理/任务二 电影数据处理/film/clean_data/clean_users.csv', index=False)

# 2. 电影数据清洗
# (1) 读取数据
movies_df = pd.read_csv('data/movies.dat', sep='::', header=None, engine='python')
movies_df.columns = ['movieID', 'title', 'genres']

# (2) 找出重复数据并保存
dup_movies = movies_df[movies_df.duplicated(keep='last')]
dup_movies.to_csv('Desktop/大数据应用与服务实训项目/数据采集与处理/任务二 电影数据处理/film/clean_data/dup_movies_data.csv', index=False)

# (3) 删除重复数据并保存
movies_df.drop_duplicates(keep='last', inplace=True)
movies_df.to_csv('Desktop/大数据应用与服务实训项目/数据采集与处理/任务二 电影数据处理/film/clean_data/clean_movies_data.csv', index=False)

# 3. 评分数据清洗
# (1) 读取数据
ratings_df = pd.read_csv('data/ratings.dat', sep='::', header=None, engine='python')
ratings_df.columns = ['userID', 'movieID', 'rating', 'timestamp']

# (2) 用用户的平均评分填充缺失值
ratings_df['rating'].fillna(ratings_df.groupby('userID')['rating'].transform('mean').round(0), inplace=True)
ratings_df.to_csv('Desktop/大数据应用与服务实训项目/数据采集与处理/任务二 电影数据处理/film/clean_data/filled_rating_data.csv', index=False)

# (3) 合并数据
merged_df = pd.merge(pd.merge(users_df, ratings_df, on='userID'), movies_df, on='movieID')
# 替换性别
merged_df['gender'] = merged_df['gender'].map({'female': 0, 'male': 1})
merged_df.to_csv('Desktop/大数据应用与服务实训项目/数据采集与处理/任务二 电影数据处理/film/clean_data/merged_data.csv', index=False)

# (4) 增加'rating'列并保存
movies_df['rating'] = ratings_df.groupby('movieID')['rating'].mean().round(0).astype(int)
movies_df.to_csv('Desktop/大数据应用与服务实训项目/数据采集与处理/任务二 电影数据处理/film/clean_data/movies_add_rating.csv', index=False)

# 打印前10条数据
print(movies_df.head(10))
