import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
import sklearn.linear_model as linear_model

#constante
areas=[ 'MT' , 'CH' , 'CN' , 'LC']

for area in areas:
    print(area)
    if area != 'LC':
        #abrindoo dataset
        microdados=pd.read_csv("./"+area+'2017'+'_ALVO.csv',  encoding = "ISO-8859-1", sep = ';',)#dados dos alvos
        
        y_train = microdados['NU_NOTA'].values
        
        matrizAcertos= microdados.drop(columns=['NU_INSCRICAO', 'NU_NOTA', 'NU_ACERTOS', 'CO_ESCOLA']).values
        
        columns=microdados.drop(columns=['NU_INSCRICAO', 'NU_NOTA', 'NU_ACERTOS', 'CO_ESCOLA']).columns.values
        
        microdadosGeral=pd.read_csv("./"+area+'2017.csv',  encoding = "ISO-8859-1", sep = ';',)#dados gerais
        
        #criando um vetor de scores
        scores=[]
        for item in columns:
            scores.append(sum(microdadosGeral[str(item)].values)/float(len(microdadosGeral)))
        
        #multiplicando a matrizAcertos pelo vetor de scores para obter a soma das questoes
        X_train=matrizAcertos.dot(np.array(scores).reshape(-1,1))
            
        #abrindo o dataset de test
        microdados=pd.read_csv("./"+area+'2016'+'_ALVO.csv',  encoding = "ISO-8859-1", sep = ';',)#alvo
        
        y_test = microdados['NU_NOTA'].values
        
        matrizAcertos= microdados.drop(columns=['NU_INSCRICAO', 'NU_NOTA', 'NU_ACERTOS', 'CO_ESCOLA']).values
        
        columns=microdados.drop(columns=['NU_INSCRICAO', 'NU_NOTA', 'NU_ACERTOS', 'CO_ESCOLA']).columns.values
        
        #criando um novo X_testcolocando em ordem decrescente de dificuldade as questoes
        #criando um vetor de scores
        scores=[]
        for item in columns:
            scores.append(sum(microdados[str(item)].values)/float(len(microdados)))
            
        #multiplicando a matrizAcertos pelo vetor de scores para obter a soma das questoes
        X_test=matrizAcertos.dot(np.array(scores).reshape(-1,1))
    
    else:
        y_train=[]
        y_test=[]
        X_train=[]
        X_test=[]
        for area in ['LCI', 'LCE']:
            #abrindoo dataset
            microdados=pd.read_csv("./"+area+'2017'+'_ALVO.csv',  encoding = "ISO-8859-1", sep = ';',)#dados dos alvos
            
            y_train = np.concatenate((y_train,microdados['NU_NOTA'].values))
            
            matrizAcertos= microdados.drop(columns=['NU_INSCRICAO', 'NU_NOTA', 'NU_ACERTOS', 'CO_ESCOLA']).values
            
            columns=microdados.drop(columns=['NU_INSCRICAO', 'NU_NOTA', 'NU_ACERTOS', 'CO_ESCOLA']).columns.values
            
            microdadosGeral=pd.read_csv("./"+area+'2017.csv',  encoding = "ISO-8859-1", sep = ';',)#dados gerais
            
            #criando um vetor de scores
            scores=[]
            for item in columns:
                scores.append(sum(microdadosGeral[str(item)].values)/float(len(microdadosGeral)))
            
            #multiplicando a matrizAcertos pelo vetor de scores para obter a soma das questoes
            finalScores=matrizAcertos.dot(np.array(scores).reshape(-1,1))
            if X_train==[]:
                X_train=finalScores
            else:
                X_train=np.concatenate((X_train,finalScores))
            
            #abrindo o dataset de test
            microdados=pd.read_csv("./"+area+'2016'+'_ALVO.csv',  encoding = "ISO-8859-1", sep = ';',)#alvo
            
            y_test = np.concatenate((y_test,microdados['NU_NOTA'].values))
            
            matrizAcertos= microdados.drop(columns=['NU_INSCRICAO', 'NU_NOTA', 'NU_ACERTOS', 'CO_ESCOLA']).values
            
            columns=microdados.drop(columns=['NU_INSCRICAO', 'NU_NOTA', 'NU_ACERTOS', 'CO_ESCOLA']).columns.values
            
            #criando um novo X_testcolocando em ordem decrescente de dificuldade as questoes
            #criando um vetor de scores
            scores=[]
            for item in columns:
                scores.append(sum(microdados[str(item)].values)/float(len(microdados)))
                
            #multiplicando a matrizAcertos pelo vetor de scores para obter a soma das questoes
            finalScores=matrizAcertos.dot(np.array(scores).reshape(-1,1))
            if X_test==[]:
                X_test=finalScores=matrizAcertos.dot(np.array(scores).reshape(-1,1))
            else:
                X_test=np.concatenate((X_test,finalScores))
    
    #fazendo com que X_test tenha mesma media e desvio que X_train
    std1=X_test.std()#desvio do test
    std2=X_train.std()#desvio do treino
    avrg1=X_test.mean()#media do test
    avrg2=X_train.mean()#media do treino
    X_test=X_test*(std2/std1)#media passa a ser de avrg1*std2/std1 e desvio passa a ser std2
    X_test=X_test+(avrg2-avrg1*std2/std1)#media passa a ser de avrg2
    
    microdados=None
    microdadosGeral=None
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


