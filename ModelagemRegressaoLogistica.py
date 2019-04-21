import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from sklearn.metrics import mean_squared_error, r2_score

#constante
areas=[ 'MT' , 'CH' , 'CN' , 'LCE', 'LCI']
ano='2017'

for area in areas:
    print(area)
    #abrindoo dataset
    microdados=pd.read_csv("./"+area+ano+'.csv',  encoding = "ISO-8859-1", sep = ';',)

    #alvo
    nota_real = microdados['NU_NOTA'].values


    #algumas informacoes sobre o alvo
    n_participantes  = np.size(nota_real)
    media_nota_real  = np.mean(nota_real)
    desvio_nota_real = np.std(nota_real)

    print ( '  Numero de Participantes      = %d\n'     % n_participantes  )
    print ( '  Media  da Nota Real          =   %.4f  ' % media_nota_real  )
    print ( '  Desvio da Nota Real          =   %.4f\n' % desvio_nota_real )

    #variavel a ser utilizada
    qtd_acertos=microdados['NU_ACERTOS'].values

    #algumas informacoes sobre a quantidade de acertos
    media_acertos  = np.mean(qtd_acertos)
    desvio_acertos = np.std(qtd_acertos) 

    print ( '  Media  do Numero de Acertos  =   %.4f  ' % media_acertos    )
    print ( '  Desvio da Numero de Acertos  =   %.4f\n' % desvio_acertos )

    #plt.scatter(qtd_acertos, nota_real)
    #plt.show()

    theta = ( qtd_acertos - media_acertos ) / desvio_acertos

    #matriz contendo os acertos
    acerto = microdados.drop(columns=['NU_INSCRICAO', 'NU_NOTA', 'NU_ACERTOS']).values


    #------------------------------------------------------------------------------
    #  INICIO DO PROCESSO ITERATIVO DE ESTIMACAO DA NOTA (parametro theta)
    #------------------------------------------------------------------------------

    for iter in range(30) :

        #------------------------------------------------------------------------------
        #  Calcular RMSE entre a nota estimada e a nota real
        #------------------------------------------------------------------------------
        
        nota_estimada = theta * 100 + 500

        print ( '\nITERACAO %d :' % iter                                                       )
        print ( 'RMSE = %.3f'     % math.sqrt(mean_squared_error ( nota_real , nota_estimada )))
        print ( 'R2   = %.3f\n'   %                     r2_score ( nota_real , nota_estimada ) )

        #------------------------------------------------------------------------------
        #
        #  Otimizar a(i), b(i) e c(i) para os valores atuais de t(j):
        #
        #                         1 - c(i)
        #    c(i) + --------------------------------------- = p(j,i)
        #            1 + exp ( -a(i) * (t(j) - b(i)) )
        #
        #  Considerando c igual a 0 :
        #
        #                     1
        #    --------------------------------------- = p(j,i)
        #     1 + exp ( -a(i) * (theta(j) - b(i)) )
        #
        #------------------------------------------------------------------------------
                
        from sklearn.linear_model import LogisticRegression

        lr = LogisticRegression(penalty='l2', C=1)
        
        a = np.zeros((45))
        b = np.zeros((45))
        
        for i in range(45) :
            lr.fit ( theta.reshape(-1,1) , acerto[:,i] )
            a[i] = lr.coef_[0]
            b[i] = -lr.intercept_ / a[i]
            
        lr = LogisticRegression(penalty='l2', C=1, fit_intercept=False)

        ALPHA = 0.125    
        for j in range(n_participantes) :
            if np.sum(acerto[j,:]) == 0 :
                print (' j = %d\n' % j )
                continue
            lr.fit ( a.reshape(-1,1) , acerto[j,:] )
            thetaj   = lr.coef_[0] + b[i]
            theta[j] = theta[j] + ALPHA * (thetaj-theta[j])
 
