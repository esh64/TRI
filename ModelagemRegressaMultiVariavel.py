import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
import sklearn.linear_model as linear_model
from sklearn.svm import SVR

#constante
areas=[ 'MT' , 'CH' , 'CN' , 'LCE', 'LCI']
ano='2017'
for area in areas:
    print(area)
    #abrindoo dataset
    microdados=pd.read_csv("./"+area+ano+'.csv',  encoding = "ISO-8859-1", sep = ';',)

    nota_real = microdados['NU_NOTA'].values

    acerto = microdados.drop(columns=['NU_INSCRICAO', 'NU_NOTA', 'NU_ACERTOS']).values

    X_train, X_test, y_train, y_test = train_test_split(acerto, nota_real, test_size=0.3, random_state=55)

    #-------------------------Modelando-------------------------------------------

    #SVR = SVR()
    #SVR.fit(X_train, np.log1p(y_train))
    #y_pred = np.expm1(SVR.predict(X_test))
    #print('RMSE SVR RBF', np.sqrt(mean_squared_error(y_test, y_pred)))
    #print('R2 SVR RBF', r2_score(y_test, y_pred))
    #SVR=0

    #SVR1 = SVR(kernel='poly', degree=1)
    #SVR1.fit(X_train, np.log1p(y_train))
    #y_pred = np.expm1(SVR1.predict(X_test))
    #print('RMSE SVR p1', np.sqrt(mean_squared_error(y_test, y_pred)))
    #print('R2 SVR p1', r2_score(y_test, y_pred))
    #SVR1=0

    #SVR1 = SVR(kernel='poly', degree=2)
    #SVR2.fit(X_train, np.log1p(y_train))
    #y_pred = np.expm1(SVR2.predict(X_test))
    #print('RMSE SVR p2', np.sqrt(mean_squared_error(y_test, y_pred)))
    #print('R2 SVR p2', r2_score(y_test, y_pred))
    #SVR2=0

    #SVR1 = SVR(kernel='poly', degree=3)
    #SVR3.fit(X_train, np.log1p(y_train))
    #y_pred = np.expm1(SVR3.predict(X_test))
    #print('RMSE SVR p3', np.sqrt(mean_squared_error(y_test, y_pred)))
    #print('R2 SVR p3', r2_score(y_test, y_pred))
    #SVR3=0


    lasso = linear_model.LassoLarsCV(max_n_alphas=pow(10,50),cv=300,n_jobs=-1)
    lasso.fit(X_train, np.log1p(y_train))
    y_pred = np.expm1(lasso.predict(X_test))
    print('RMSE lasso', np.sqrt(mean_squared_error(y_test, y_pred)))
    print('R2 lasso', r2_score(y_test, y_pred))
    lasso=0

    random_forest = RandomForestRegressor(max_depth=None ,n_estimators=3750, n_jobs=-1)
    random_forest.fit(X_train, np.log1p(y_train))
    y_pred = np.expm1(random_forest.predict(X_test))
    print('RMSE RF', np.sqrt(mean_squared_error(y_test, y_pred)))
    print('R2 RF', r2_score(y_test, y_pred))
    random_forest=0

    xgbr = xgb.XGBRegressor(colsample_bytree=0.4,gamma=0,            learning_rate=0.0007,max_depth=12,min_child_weight=1.5,n_estimators=5000,                                                                    reg_alpha=0.75,reg_lambda=0.45,subsample=0.6,seed=42,n_jobs=-1)
    xgbr.fit(X_train,np.log1p(y_train))
    Ypredxgbr = np.expm1(xgbr.predict(X_test))
    print('RMSE xgbr',np.sqrt(mean_squared_error(y_test, y_pred)))
    print('R2 xgbr', r2_score(y_test, y_pred))
 
