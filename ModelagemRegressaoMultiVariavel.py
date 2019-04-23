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
    microdados=pd.read_csv("./"+area+'2017'+'_ALVO.csv',  encoding = "ISO-8859-1", sep = ';',)#dados dos alvos
    
    y_train = microdados['NU_NOTA'].values
    
    columns=microdados.drop(columns=['NU_INSCRICAO', 'NU_NOTA', 'NU_ACERTOS', 'CO_ESCOLA']).columns.values#nome das colunas
    
    microdadosGeral=pd.read_csv("./"+area+'2017.csv',  encoding = "ISO-8859-1", sep = ';',)#dados gerais
    
    #criando um novo X_train colocando em ordem decrescente de dificuldade as questoes
    ranking={}
    count=1
    for item in columns:
        key=str(sum(microdadosGeral[str(item)].values)/float(len(microdadosGeral)))
        if key in ranking.keys():
            key+=str(count)
            count+=1
        ranking[key]=microdados[str(item)].values.reshape(-1,1)
    
    X_train=[]
    for value in sorted(ranking.keys()):
        if X_train==[]:
            X_train=ranking[value]
        else:
            X_train=np.append(X_train, ranking[value], axis=1)
        
    #abrindo o dataset de test
    microdados=pd.read_csv("./"+area+'2016_ALVO.csv',  encoding = "ISO-8859-1", sep = ';',)#alvo
    
    y_test = microdados['NU_NOTA'].values
    
    columns=microdados.drop(columns=['NU_INSCRICAO', 'NU_NOTA', 'NU_ACERTOS', 'CO_ESCOLA']).columns.values#nome das colunas

    #dados gerais
    #microdadosGeral=pd.read_csv("./"+area+'2016.csv',  encoding = "ISO-8859-1", sep = ';',)
    
    #criando um novo X_testcolocando em ordem decrescente de dificuldade as questoes
    ranking={}
    count=1
    for item in columns:
        key=str(sum(microdados[str(item)].values)/float(len(microdados)))
        if key in ranking.keys():
            key+=str(count)
            count+=1
        ranking[key]=microdados[str(item)].values.reshape(-1,1)
        
    X_test=[]
    for value in sorted(ranking.keys()):
        if X_test==[]:
            X_test=ranking[value]
        else:
            X_test=np.append(X_test, ranking[value], axis=1)
    
    microdados=None

    #-------------------------Modelando-------------------------------------------

    CV=10
    if len(y_train)<10:
        CV=len(y_train)
    lasso = linear_model.LassoLarsCV(max_n_alphas=pow(10,60),cv=CV,n_jobs=-1)
    lasso.fit(X_train, np.log1p(y_train))
    y_pred = np.expm1(lasso.predict(X_test))
    print('RMSE lasso', np.sqrt(mean_squared_error(y_test, y_pred)))
    print('R2 lasso', r2_score(y_test, y_pred))
    lasso=0
    
    
    ridge = linear_model.RidgeCV(alphas=[pow(10, -x) for x in range(5,20)],cv=CV) 
    ridge.fit(X_train, np.log1p(y_train))
    y_pred = np.expm1(ridge.predict(X_test))
    print('RMSE ridge', np.sqrt(mean_squared_error(y_test, y_pred)))
    print('R2 ridge', r2_score(y_test, y_pred))
    ridge=0
    
    #ENET = linear_model.ElasticNetCV(n_alphas=pow(10,2),cv=CV,n_jobs=-1)
    #ENET.fit(X_train, np.log1p(y_train))
    #y_pred = np.expm1(ENET.predict(X_test))
    #print('RMSE ENET', np.sqrt(mean_squared_error(y_test, y_pred)))
    #print('R2 ENET', r2_score(y_test, y_pred))
    #ENET=0

    random_forest = RandomForestRegressor(max_depth=None ,n_estimators=5000, n_jobs=-1)
    random_forest.fit(X_train, np.log1p(y_train))
    y_pred = np.expm1(random_forest.predict(X_test))
    print('RMSE RF', np.sqrt(mean_squared_error(y_test, y_pred)))
    print('R2 RF', r2_score(y_test, y_pred))
    random_forest=0

    xgbr = xgb.XGBRegressor(colsample_bytree=0.4,gamma=0,            learning_rate=0.0007,max_depth=16,min_child_weight=1.5,n_estimators=10000,                                                                    reg_alpha=0.75,reg_lambda=0.45,subsample=0.6,seed=42,n_jobs=-1)
    xgbr.fit(X_train,np.log1p(y_train))
    Ypredxgbr = np.expm1(xgbr.predict(X_test))
    print('RMSE xgbr',np.sqrt(mean_squared_error(y_test, y_pred)))
    print('R2 xgbr', r2_score(y_test, y_pred))


