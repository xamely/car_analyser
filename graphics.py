import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from statsmodels.formula.api import ols

df = pd.read_csv('cars.csv')

# Построение диаграмм рассеяния
# colns_c = 3
# fig, axes = plt.subplots(nrows=2, ncols=colns_c, figsize=(20, 10))
# features = ['Пробег',
# 			'Год выпуска',
# 			'Мощность',
#        		'Кузов',
#        		'Расход']
# for idx, feat in  enumerate(features):
#     sns.scatterplot(x='Цена', y=feat, data=df, ax=axes[idx // colns_c, idx % colns_c])
#     axes[idx // colns_c, idx % colns_c].legend()
#     axes[idx // colns_c, idx % colns_c].set_xlabel('Цена')
#     axes[idx // colns_c, idx % colns_c].set_ylabel(feat)


# Построение графика после исключения выбросов
# data = pd.read_csv('cars.csv')
# data = data[data['Класс'] != '4']
# data = data[(data['Привод'] == 'задний') | (data['Привод'] == 'передний') | (data['Привод'] == 'полный')]
# print(data.shape)
# m = ols('Цена ~ Класс',data).fit()
# infl = m.get_influence()
# sm_fr = infl.summary_frame()
# df = data[sm_fr['dffits'] < 1.24]
# print(df.shape)
# colns_c = 3
# features = ['Мощность']
# sns.scatterplot(x='Цена', y=features[0], data=df)


# Расчет ошибок модели
m = ols('Цена ~ Мощность',df).fit().resid
sns.scatterplot(x='Мощность', y=m, data=df)


# Построение Q-Q Plot
# import statsmodels.api as sm
# m = ols('Цена ~ Мощность',df).fit().resid
# sm.qqplot(m, line='s')

plt.show()

