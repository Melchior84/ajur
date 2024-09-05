import pandas as pd

arquivo = r"C:\Temp\processos.xlsx"

dados = pd.read_excel(arquivo)

totalLinhas = dados.shape[0]
print('Total de linhas do arquivo: ' + str(totalLinhas))

for indice, linha in dados.iterrows():
    print(f'Linha ({indice}) - {linha['Matrícula']} - {linha['processo']} - {linha['Nome']} - {linha['site']}')
    if indice == 10:
       break

