import sys
import pandas as pd
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import urllib2
import json 

class mainFrame(QWidget):
   def __init__(self, parent = None):
      super(mainFrame, self).__init__(parent)
      
      layout = QVBoxLayout()
      self.le = QLabel("Escolha um arquivo CSV com os Acertos em cada area, Codigo do aluno e Codigo da escola.")
      self.le.setAlignment(Qt.AlignCenter)
      layout.addWidget(self.le)
      
      self.label = QLabel('')
      self.label.setAlignment(Qt.AlignCenter)
      layout.addWidget(self.label)
      
      self.btn1 = QPushButton("Abrir Arquivo")
      self.btn1.clicked.connect(self.getfilename)
      layout.addWidget(self.btn1)

      self.setLayout(layout)
      self.setWindowTitle("POC ENEM")
      self.resize(320, 240)
      
   def getfilename(self):
      self.btn1.setEnabled(False)
      fname = str(QFileDialog.getOpenFileName())
      print("Lendo Arquivo...")
      self.le.setText('')
      self.label.setText("Lendo Arquivo...")
      qApp.processEvents()
      try:
          arquivo = pd.read_csv(fname)
      except:
          print("Arquivo corrompido")
          self.le.setText("Escolha um arquivo CSV com os Acertos em cada area, Codigo do aluno e Codigo da escola.")
          self.label.setText("Arquivo corrompido")
          self.btn1.setEnabled(True)
          return
      codigoAluno=pegarCodigo(arquivo, 'NU_INSCRICAO')
      codigoEscola=pegarCodigo(arquivo, 'CO_ESCOLA')
      acertosMT=pegarAcertos(arquivo, 'NU_ACERTOS_MT')
      acertosCN=pegarAcertos(arquivo, 'NU_ACERTOS_CN')
      acertosCH=pegarAcertos(arquivo, 'NU_ACERTOS_CH')
      acertosLC=pegarAcertos(arquivo, 'NU_ACERTOS_LC')
      urlMT='https://ussouthcentral.services.azureml.net/workspaces/0ebbbdf58aee4cd7a96eeca8a0e6b227/services/9f6982f652b1477982ad6b489c344d38/execute?api-version=2.0&details=true'
      api_keyMT='52uBXerKrEhblAY9HHUFp7frO3NroPkLReSIGk9LxmOp8P+V3voksn83sEXew1d7g7Vw6BikxUIowHeyR8nPxA=='
      print("Enviado os acertos em MT...")
      self.label.setText("Enviado os acertos em MT...")
      qApp.processEvents()
      notasMT=sendRequest(acertosMT,urlMT,api_keyMT, 'MT')
      urlCN='https://ussouthcentral.services.azureml.net/workspaces/0ebbbdf58aee4cd7a96eeca8a0e6b227/services/46a68c75fabe40f4982cc6823f56a113/execute?api-version=2.0&details=true '
      api_keyCN='uM/CQE1Njsb9ic2Ni1GGx13EIilcoz7iwGbl/tvZiAt+93dN/L9POEYXKFGugsFdiBMOFO828nWpiMphxX4Slg=='
      print("Enviado os acertos em CN...")
      self.label.setText("Enviado os acertos em CN...")
      qApp.processEvents()
      notasCN=sendRequest(acertosCN,urlCN,api_keyCN,'CN')
      urlLC='https://ussouthcentral.services.azureml.net/workspaces/0ebbbdf58aee4cd7a96eeca8a0e6b227/services/4afedd9e39f34a339d022966e093ff6f/execute?api-version=2.0&details=true'
      api_keyLC='StdDGu8yOko0W+vyliOht7Ahk8oU1qCI/RdDi7Nbo4rRxgu5TO+F3ADyI6mYV5W6w7iqAX3L679qwWd3TpdUwQ=='
      print("Enviado os acertos em LC...")
      self.label.setText("Enviado os acertos em LC...")
      qApp.processEvents()
      notasLC=sendRequest(acertosLC,urlLC,api_keyLC,'LC')
      urlCH='https://ussouthcentral.services.azureml.net/workspaces/0ebbbdf58aee4cd7a96eeca8a0e6b227/services/4f8b00071ec04a969e7d62e7c6687ccd/execute?api-version=2.0&details=true '
      api_keyCH='pVOu2vgQwGb19oavtO/Iv6zMpP9kAUZL/I5w/bjA/+JRGF+iEbQasi5uHfT9f+HdqE3i8kw9u16+zvpCosQ/Ng=='
      print("Enviado os acertos em CH...")
      self.label.setText("Enviado os acertos em CH...")
      qApp.processEvents()
      notasCH=sendRequest(acertosCH,urlCH,api_keyCH, 'CH')
      print("Escrevendo o arquivo NOTAS.CSV...")
      self.label.setText("Escrevendo o arquivo NOTAS.CSV...")
      qApp.processEvents()
      escreverArquivos(notasLC, notasMT, notasCH, notasCN, codigoAluno, codigoEscola, acertosMT,acertosLC, acertosCH, acertosCN)
      print("Arquivo NOTAS.CSV escrito com sucesso")
      self.le.setText("Escolha um arquivo CSV com os Acertos em cada area, Codigo do aluno e Codigo da escola.")
      self.label.setText("Arquivo NOTAS.CSV escrito com sucesso!")
      self.btn1.setEnabled(True)

def pegarAcertos(arquivo, area):
    values=[]
    for acerto in arquivo[area]:
        values.append(['0','0','0',str(acerto)])
    return values

def pegarCodigo(arquivo, area):
    values=[]
    for codigo in arquivo[area]:
        values.append(codigo)
    return values

def escreverArquivos(notasLC, notasMT, notasCH, notasCN,codigoAluno,codigoEscola,acertosMT,acertosLC, acertosCH, acertosCN):
    newFile=open('NOTAS.csv', 'w')
    newFile.write('CO_ALUNO;CO_ESCOLA;NU_ACERTOS_LC;NOTA_LC;NU_ACERTOS_MT;NOTA_MT;NU_ACERTOS_CH;NOTA_CH;NU_ACERTOS_CN;NOTA_CN\n')
    for index in range(len(notasLC)):
        newFile.write(str(codigoAluno[index])+';'+str(codigoEscola[index])+';'+str(acertosLC[index][-1])+';'+str(notasLC[index])+';'+str(acertosMT[index][-1])+';'+str(notasMT[index])+';'+str(acertosCH[index][-1])+';'+str(notasCH[index])+';'+str(acertosCN[index][-1])+';'+str(notasCN[index])+'\n')
    newFile.close()

def sendRequest(values, url, api_key, area):
    data =  {
            "Inputs": {

                    "input1":
                    {
                        "ColumnNames": ["NU_INSCRICAO", "CO_ESCOLA", "NU_NOTA", "NU_ACERTOS"],
                        "Values": values
                    },        },
                "GlobalParameters": {
            "Append score columns to output": "False",
    }
        }

    body = str.encode(json.dumps(data))

     # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib2.Request(url, body, headers) 

    try:
        response = urllib2.urlopen(req)

        # If you are using Python 3+, replace urllib2 with urllib.request in the above code:
        # req = urllib.request.Request(url, body, headers) 
        # response = urllib.request.urlopen(req)

        result = response.read()
        json1_data = json.loads(result)
        if area=='CH':
            return [float(x[0]) for x in json1_data[u'Results'][u'output1'][u'value'][u'Values']]
        return [float(x[2]) for x in json1_data[u'Results'][u'output1'][u'value'][u'Values']]
    
    except urllib2.HTTPError, error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())

        print(json.loads(error.read()))



def main():
   app = QApplication(sys.argv)
   ex = mainFrame()
   ex.show()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()
