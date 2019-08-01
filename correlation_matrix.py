import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('cars.csv')
df = df[df['Класс автомобиля'] != '4']
df = df[df['Класс автомобиля'] != 'J']
df = df[(df['Привод'] == 'задний') | (df['Привод'] == 'передний') | (df['Привод'] == 'полный')]
df = df.drop('Модель', 1)
df = df.drop('Цвет', 1)
df = df.drop('Страна марки', 1)

df_dm = pd.get_dummies(df, drop_first=True) # замена текстовых переменных на числовые

corr = df_dm.corr()
fig, ax = plt.subplots()
ax.matshow(corr, cmap='seismic')

for (i, j), z in np.ndenumerate(corr):
    ax.text(j, i, '{:0.2f}'.format(z), ha='center', va='center')

plt.xticks(range(len(corr.columns)), corr.columns, rotation = 90)
plt.yticks(range(len(corr.columns)), corr.columns)
plt.show()