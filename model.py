import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.formula.api import ols

from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
import time


start_time = time.time()

data = pd.read_csv('cars.csv')
data = data[data['Класс'] != '4']
data = data[(data['Привод'] == 'задний') | (data['Привод'] == 'передний') | (data['Привод'] == 'полный')]

m = ols('Цена ~ Класс',data).fit()
infl = m.get_influence()
sm_fr = infl.summary_frame()
df = data[sm_fr['dffits'] < 1.24]

df_dm = pd.get_dummies(df, drop_first=True)

x = df_dm.drop('Цена', 1)
x_imp = SimpleImputer(missing_values=np.nan, strategy="median").fit_transform(x)
y = df_dm['Цена']

x_train, x_test, y_train, y_test = train_test_split(x_imp, y, test_size=0.45, random_state=24)

# lr = LinearRegression().fit(x_train, y_train)
# r21 = lr.score(x_train, y_train)
# r2 = lr.score(x_test, y_test)

# ridge = Ridge().fit(x_train, y_train)
# r21 = ridge.score(x_train, y_train)
# r2 = ridge.score(x_test, y_test)

# tree = RandomForestRegressor(n_estimators=100, n_jobs=-1, random_state=17)
# gm_cv = GridSearchCV(tree, {'max_depth': range(11, 12)},cv = 5)
# gm_cv.fit(x_train, y_train)
# r21 = gm_cv.score(x_train, y_train)
# r2 = gm_cv.score(x_test, y_test)

gm_cv = GridSearchCV(Ridge(), {'alpha': np.logspace(-5,8,15)},cv = 5)
gm_cv.fit(x_train, y_train)
r21 = gm_cv.score(x_train, y_train)
r2 = gm_cv.score(x_test, y_test)

# gbrt = GradientBoostingRegressor(random_state=0, n_estimators=100)
# gbrt.fit(x_train, y_train)
# gm_cv = GridSearchCV(gbrt, {'max_depth': range(1, 5)},cv = 5)
# gm_cv.fit(x_train, y_train)
# result_train = gm_cv.score(x_train, y_train)
# result_test = gm_cv.score(x_test, y_test)

print("--- %s seconds ---" % (time.time() - start_time))

for i in range(10):
    a = int(gm_cv.predict(x_test[i].reshape(1,-1))[0])
    # a = int(model.predict(x_train.iloc[[i]])[0])
    b = int(y_test.iloc[i])
#    if abs(int(a-b)) < 10000
    print('predict: ', a)
    print('real:    ', b)
    print('dif: ', abs(a-b))
    print('--------------------')
print("Alpha: {}".format(gm_cv.best_params_))
print("Правильность на обучающем наборе: {}".format(r21))
print("Правильность на тестовом наборе: {}".format(r2))

