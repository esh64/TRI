﻿Instruções de uso:
1)Abra o executável chamado mainFrame
2)Escolha um arquivo CSV com os campos NU_INSCRICAO, CO_ESCOLA, NU_ACERTOS_[MT, CH, CN e LC](2015, 2016 e 2017.csv encontrados dentro da propria dist/mainFrame)
3)Será criado um arquivo chamado NOTAS.CSV na pasta onde o executável está(dist/mainFrame)

Meio alternativo de usar:
1)Ter as bibliotecas PyQt4 e o pandas compativéis com o interpretador Python2.7
2)Execute o script mainFrame.py com um interpretador Python2.7
3)Escolha um arquivo CSV com os campos NU_INSCRICAO, CO_ESCOLA, NU_ACERTOS_[MT, CH, CN e LC](2015, 2016 e 2017.csv encontrados dentro da propria dist/mainFrame)
4)Será criado um arquivo chamado NOTAS.CSV na pasta onde o executável está(dist/mainFrame)

Arquivo CSV de entrada:
NU_INSCRICAO é o equivalente a um código de aluno, nos arquivos de exemplo, o número de inscrição no ENEM
CO_ESCOLA é o código da escola/unidade 
NU_ACERTOS_ é a quantidade de acertos em uma prova decada área
Cada linha corresponde a um aluno
O arquivo de entrada deve corresponder à uma população na ordem de 660 alunos, poucas amostras não garantirá um resultado acurado

Arquivo CSV de saida:
NU_INSCRICAO e CO_ESCOLA são as mesmas colunas da entrada
NU_NOTA_ é a nota em cada área.
