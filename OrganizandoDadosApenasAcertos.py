import pandas as pd
import numpy as np
import sys

#entrada do usuario
ano=sys.argv[-1]

#------------------------------------------
#este programa tem como objetivo criar um arquivo CSV para cada area do conhecimento, sendo que as colunas o numero de inscricao, nota, codigo da questao e total de acertos
#os valores mencionados em constantes devem ser adicionados novas provas

#constantes

MICRODADOS_2017_URL='./Microdados Enem 2017/DADOS/MICRODADOS_ENEM_2017.csv'
MICRODADOS_2016_URL='./Microdados_enem_2016/DADOS/microdados_enem_2016.csv'
MICRODADOS_2015_URL='./Microdados_enem_2015/DADOS/MICRODADOS_ENEM_2015.csv'
areas=[ 'MT' , 'CH' , 'CN' , 'LC' ]
codigos_prova={'2015':{},'2016':{},'2017':{}}
#codigo das provas relevantes: azul, amarela, rosa e branca
codigos_prova['2017']['CN']=[391, 392, 393, 394]
codigos_prova['2017']['CH']=[395, 396, 397, 398]
codigos_prova['2017']['LC']=[399, 400, 401, 402]
codigos_prova['2017']['MT']=[403, 404, 405, 406] 
codigos_prova['2016']['CN']=[291, 292, 293, 294]
codigos_prova['2016']['CH']=[295, 296, 297, 298]
codigos_prova['2016']['LC']=[299, 300, 301, 302]
codigos_prova['2016']['MT']=[303, 304, 305, 306]
codigos_prova['2015']['CN']=[235, 236, 237, 238]
codigos_prova['2015']['CH']=[231, 232, 233, 234]
codigos_prova['2015']['LC']=[239, 240, 241, 242]
codigos_prova['2015']['MT']=[243, 244, 245, 246]
separador={'2015':',','2016':';' ,'2017':';'}

MICRODADOS_URL={'2015':MICRODADOS_2015_URL,'2016':MICRODADOS_2016_URL, '2017':MICRODADOS_2017_URL}

#________________Inicio do programa

#abrindo dataset por area 
for areaM in areas:
    area=areaM
    if 'LC' in areaM:
        area='LC'
    #escrevendo um novo arquivo CSV que contera numero de inscricao, nota, itens(codigo) e total de acerto
    newFile=open(areaM+ano+"ApenasAcertos.csv", 'w')
    #escrevendo o cabecalho
    newFile.write('NU_INSCRICAO,CO_ESCOLA,NU_NOTA,NU_ACERTOS\n')
    #cabecalho pronto
    
    #importando os microdados
    microdados = pd.read_csv( MICRODADOS_URL[ano], encoding = "ISO-8859-1",sep =separador[ano],usecols=['CO_ESCOLA','NU_INSCRICAO','TP_PRESENCA_'+area,'CO_PROVA_'+area,'NU_NOTA_'+area,'TX_RESPOSTAS_'+area,'TX_GABARITO_'+area, 'TP_LINGUA']).dropna()#essa parte esta um pouco ruim, pois e necessario ler o dataset para cada prova
    
    #escreverei cada linha de microdados no novo arquivo
    numero_linhasObtidas=len(microdados.values)
    for linha in range(numero_linhasObtidas):
        
        #eliminado o candidato do novo arquivo
        if microdados['CO_PROVA_'+area].values[linha] not in codigos_prova[ano][area]:#se o codigo da prova nao for relevante
            continue
        if (areaM=='LCI' and microdados['TP_LINGUA'].values[linha]==1) or (areaM=='LCE' and microdados['TP_LINGUA'].values[linha]==0):#condidato nao entrara no arquivo da lingua que nao fez prova
            continue
        if microdados['TP_PRESENCA_'+area].values[linha]!=1: #candidato nao recebeu nota na prova
            continue
        respostas=microdados['TX_RESPOSTAS_'+area].values[linha]
      
        if '*' in respostas or '.' in respostas:#se o candidato deixou alguma questao em branco, sera descartado
            continue
        gabarito=microdados['TX_GABARITO_'+area].values[linha]

        
        #----Comecando a escrever no arquivo
        #primeira coluna: numero inscricao
        newFile.write(str(microdados.NU_INSCRICAO.values[linha])+',')
        #segunda coluna: codigo da escola
        newFile.write(str(microdados.CO_ESCOLA.values[linha])+',')
        #terceira coluna: nota
        newFile.write(str(microdados['NU_NOTA_'+area].values[linha])+',')
        #proximas colunas: questoes
        quantidade_acertos=0
        for i in range(len(respostas)):
            if respostas[i]==gabarito[i]:
                quantidade_acertos+=1
        newFile.write(str(quantidade_acertos)+'\n')
        #------fim da linha
    newFile.close()
    #arquivo escrito
