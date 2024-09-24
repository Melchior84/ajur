import time
import base64
import os
import pandas as pd

from codeKey import codigo_Melk

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from anticaptchaofficial.imagecaptcha import *
from PIL import Image
from io import BytesIO
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

total = 0
sucesso = 0
problemas = 0


def main():   
    global total 
    global sucesso
    global problemas

    arquivo = r"C:\Temp\processos.xlsx"
    dados = pd.read_excel(arquivo)
    totalLinhas = dados.shape[0]
    print('Total de linhas do arquivo: ' + str(totalLinhas))   


    for indice, linha in dados.iterrows():
        print(f'Registro ({indice}) - {linha['Matrícula']} - {linha['processo']} - {linha['Nome']} - {linha['site']}')
        total = total + 1

        url = linha['site']
        processo = linha['processo']

        navegador = webdriver.Firefox()
        navegador.get(url)
        aguardar = WebDriverWait(navegador, 100)

        input_numero_processo = aguardar.until(EC.presence_of_element_located((By.ID, "nrProcessoInput")))
        input_numero_processo.send_keys(processo)

        botao_pesquisar = navegador.find_element(By.ID, "btnPesquisar")
        botao_pesquisar.click()
        time.sleep(2)

        try:       

            h1 = navegador.find_element(By.XPATH, "/html/body/pje-root/main/pje-lista-processo/div[1]/h1")
            qtd_processos = h1.text

            if "0 processos encontrados" in qtd_processos:
                print("Nenhum processo encontrado")
                problemas = problemas + 1
            elif "1 processos encontrados" in qtd_processos:
                print("Um processo encontrado")
            elif "2 processos encontrados" in qtd_processos:
                print("Dois processos encontrados")
            else:
                print("Texto não encontrado com a quantidade de processos ou valor inesperado")    
                problemas = problemas + 1
            try:
                botao_primeiro_grau = botao_pesquisar = navegador.find_element(By.XPATH, "/html/body/pje-root/main/pje-lista-processo/div[1]/button[1]")
                botao_primeiro_grau.click()

                time.sleep(2)

                captcha(navegador)

                navegador.quit()

            except NoSuchElementException:
                navegador.quit()

        except NoSuchElementException:

            try:
                navegador.find_element(By.XPATH, '//*[@id="painelCaptcha"]')
                captcha(navegador)
            except NoSuchElementException:
                print("Entrou no captcha e não localizou o elemento")
                problemas = problemas + 1
            
        except ElementClickInterceptedException:
            print("Não foi possível clicar no botão")
            problemas = problemas + 1

        finally:
            # Fecha o WebDriver
            navegador.quit()
        
        if indice == 10:
            print("Atividade finalizada com sucesso.")
            print("Sucesso: " + str(sucesso))
            print("Erro: " + str(problemas))
            print("Total: " + str(total))
            break


def captcha(navegador):

    global total 
    global sucesso
    global problemas

    solver = imagecaptcha()
    solver.set_verbose(0)
    solver.set_key(codigo_Melk())
    solver.set_soft_id(0)

    img = navegador.find_element(By.ID, "imagemCaptcha")
    base64_string = img.get_attribute('src')

    imagem = base64_string.split(",", 1)

    image_bytes = base64.b64decode(imagem[1])

    caminho_destino = r"C:\Users\prvf56\OneDrive - PREVI\Projetos\Ajur\captcha.jpg"
    
    with open(caminho_destino, "wb") as arquivo:
        arquivo.write(image_bytes)

    #print(f"Imagem salva em {caminho_destino}")

    captcha_text = solver.solve_and_return_solution("captcha.jpg")

    if captcha_text != 0:
        print("Texto Captcha: "+captcha_text)
        navegador.find_element(By.ID, "captchaInput").send_keys(captcha_text)
        navegador.find_element(By.ID, "btnEnviar").click()
        time.sleep(1)
        navegador.find_element(By.ID, "btnDownloadIntegra").click()
        time.sleep(7)
        print("Arquivo salvo com sucesso.")
        sucesso = sucesso + 1

    else:
        print("Tarefa Captcha Finalizou com erro: "+solver.error_code)
        problemas = problemas + 1

if __name__ == "__main__":
    main()