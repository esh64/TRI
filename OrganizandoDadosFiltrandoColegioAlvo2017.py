import pandas as pd
import numpy as np

#------------------------------------------
#este programa tem como objetivo criar um arquivo CSV para cada area do conhecimento, sendo que as colunas o numero de inscricao, nota, codigo da questao e total de acertos
#os valores mencionados em constantes devem ser alterados para mudar o ano da prova ou mudar o numero de linhas usados

#constantes
MICRODADOS_2017_URL='./Microdados Enem 2017/DADOS/MICRODADOS_ENEM_2017.csv'
ITENSPROVA_2017_URL='./Microdados Enem 2017/DADOS/ITENS_PROVA_2017.csv'
areas=[ 'MT' , 'CH' , 'CN' , 'LC' ]
codigos_prova={}
#codigo das provas relevantes: azul, amarela, rosa e branca !MODIFICAR CASO MODIFIQUE O ANO DA PROVA
codigos_prova['CN']=[391, 392, 393, 394]
codigos_prova['CH']=[395, 396, 397, 398]
codigos_prova['LC']=[399, 400, 401, 402]
codigos_prova['MT']=[403, 404, 405, 406] 
CO_ESCOLA=[35563006, 35286187,35134806]

#________________Inicio do programa


#preparando um mapeando para todos as provas

#dicionarios de cada area contendo os 4 codigos de provas como chave e como valor um outro dicionario que tem como chave o codigo do item e valor a posicao
questoesMT={} 
questoesCH={}
questoesCN={}
questoesLCIngles={}
questoesLCEspanhol={}

questoesAreas={'MT':questoesMT, 'CH':questoesCH, 'CN':questoesCN, 'LCI':questoesLCIngles, 'LCE':questoesLCEspanhol}#dicionario com as questoes de todas as areas
codigo_itens={'CN':[], 'MT':[], 'CH':[], 'LCI':[], 'LCE':[]}#codigo dos itens

#abrindo as informacoes da prova
itens = pd.read_csv( ITENSPROVA_2017_URL, encoding = "ISO-8859-1", sep = ';', usecols=['CO_PROVA','CO_POSICAO','CO_ITEM','SG_AREA', 'TP_LINGUA'])

#fazendo o mapeamento de cada item nas diferentes provas
for areaM in questoesAreas.keys():
    area=areaM
    if 'LC' in areaM:
        area='LC'
    for codigo_prova in codigos_prova[area]:
        #armazenando os codigos dos itens
        if codigo_itens[areaM]==[]:
            if areaM=='LCI':#se a prova for de ingles
                codigo_itens[areaM]=np.concatenate((itens[(itens.CO_PROVA==codigo_prova) & (itens.SG_AREA==area) & (itens.TP_LINGUA!=0) & (itens.TP_LINGUA!=1)].CO_ITEM.values,itens[(itens.CO_PROVA==codigo_prova) & (itens.SG_AREA==area) & (itens.TP_LINGUA==0)].CO_ITEM.values))
            else:
                if areaM=='LCE':#se a prova for de espanhol
                     codigo_itens[areaM]=np.concatenate((itens[(itens.CO_PROVA==codigo_prova) & (itens.SG_AREA==area) & (itens.TP_LINGUA!=0) & (itens.TP_LINGUA!=1)].CO_ITEM.values,itens[(itens.CO_PROVA==codigo_prova) & (itens.SG_AREA==area) & (itens.TP_LINGUA==1)].CO_ITEM.values))
                else:
                    codigo_itens[areaM]=itens[(itens.CO_PROVA==codigo_prova) & (itens.SG_AREA==area)].CO_ITEM.values
        questoesAreas[areaM][codigo_prova]={}
        posicoes_itens=range(1,46)#posicoes dos itens de 1 a 45
        if area=='LC':
            posicoes_itens=range(1,51)
        for posicao_item in posicoes_itens:
            #mapeamento Codigo->posicao
            codigo_item=itens[(itens.CO_PROVA==codigo_prova) & (itens.SG_AREA==area) & (itens.CO_POSICAO==posicao_item)].CO_ITEM.values[0]
            questoesAreas[areaM][codigo_prova][codigo_item]=posicao_item
            
#abrindo dataset por area 
for areaM in questoesAreas.keys():
    area=areaM
    if 'LC' in areaM:
        area='LC'
    #escrevendo um novo arquivo CSV que contera numero de inscricao, nota, itens(codigo) e total de acerto
    newFile=open(areaM+"2017_ALVO.csv", 'w')
    #escrevendo o cabecalho
    newFile.write('NU_INSCRICAO;CO_ESCOLA;NU_NOTA;')
    for codigo in codigo_itens[areaM]:
        newFile.write(str(codigo)+';')
    newFile.write('NU_ACERTOS\n')
    #cabecalho pronto
    
    #importando os microdados
    microdados = pd.read_csv( MICRODADOS_2017_URL, encoding = "ISO-8859-1",sep =';',usecols=['CO_ESCOLA','NU_INSCRICAO','TP_PRESENCA_'+area,'CO_PROVA_'+area,'NU_NOTA_'+area,'TX_RESPOSTAS_'+area,'TX_GABARITO_'+area, 'TP_LINGUA']).dropna()
    
    #escreverei cada linha de microdados no novo arquivo
    numero_linhasObtidas=len(microdados.values)
    for linha in range(numero_linhasObtidas):
        
        #eliminado o candidato do novo arquivo
        if microdados.CO_ESCOLA.values[linha]  not in CO_ESCOLA:#candidato nao e da escola alvo
            continue
        if microdados['CO_PROVA_'+area].values[linha] not in codigos_prova[area]:#se o codigo da prova nao for relevante
            continue
        if (areaM=='LCI' and microdados['TP_LINGUA'].values[linha]==1) or (areaM=='LCE' and microdados['TP_LINGUA'].values[linha]==0):#condidato nao entrara no arquivo da lingua que nao fez prova
            continue
        if microdados['TP_PRESENCA_'+area].values[linha]!=1: #candidato nao recebeu nota na prova
            continue
        respostas=microdados['TX_RESPOSTAS_'+area].values[linha]
        gabarito=microdados['TX_GABARITO_'+area].values[linha]
        if '*' in respostas or '.' in respostas:#se o candidato deixou alguma questao em branco, sera descartado
            continue
        
        #----Comecando a escrever no arquivo
        #primeira coluna: numero inscricao
        newFile.write(str(microdados.NU_INSCRICAO.values[linha])+';')
        #segunda coluna: codigo escola, apenas para checar se estou realmente pegando os dados certos
        newFile.write(str(microdados.CO_ESCOLA.values[linha])+';')
        #terceira coluna: nota
        newFile.write(str(microdados['NU_NOTA_'+area].values[linha])+';')
        #proximas colunas: questoes
        quantidade_acertos=0
        for codigo_item in codigo_itens[areaM]:
            codigo_prova=microdados['CO_PROVA_'+area].values[linha]
            posicao_item=questoesAreas[areaM][codigo_prova][codigo_item]-1
            #print(posicao_item, len(respostas), len(questoesAreas[areaM][codigo_prova]))
            if str(respostas[posicao_item]) not in 'ABCDE':#questao da lingua que o candidato nao escolheu
                continue
            if str(respostas[posicao_item])==str(gabarito[posicao_item]):
                quantidade_acertos+=1
                newFile.write('1;')#escreve 1 se acertou a questao
            else:
                newFile.write('0;')#escreve 0 se errou a questao
        #ultima coluna: quantidade de acertos
        newFile.write(str(quantidade_acertos)+'\n')
        #------fim da linha
    newFile.close()
    #arquivo escrito
