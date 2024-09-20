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

    print("-----------------------------------")
    print("  RPA Baixar Processos para AJUR   ")
    print("-----------------------------------")

    global total 
    global sucesso
    global problemas

    arquivo = r"C:\Users\prvf56\OneDrive - PREVI\Projetos\Projeto Ajur\ajur\processos.xlsx"
    dados = pd.read_excel(arquivo)
    totalLinhas = dados.shape[0]
    qtd_graus = 0

    print("-----------------------------------")
    print('Total de linhas do arquivo: ' + str(totalLinhas)) 
    print("-----------------------------------")

    for indice, linha in dados[62:].iterrows():
        print(f'Registro ({indice}) - {linha['Matrícula']} - {linha['processo']} - {linha['Nome']} - {linha['site']}')
        total = total + 1

        url = linha['site']
        processo = linha['processo']

        navegador = webdriver.Firefox()
        navegador.get(url)

        inserir_processo(navegador, processo)

        try:
            janela_original = navegador.current_window_handle      


            h1 = navegador.find_element(By.XPATH, "/html/body/pje-root/main/pje-lista-processo/div[1]/h1")
            qtd_processos = h1.text

            if "0 processos encontrados" in qtd_processos:
                print(" - Processos localizados: 0")
                qtd_graus = 0
                problemas = problemas + 1
            elif "1 processos encontrados" in qtd_processos:
                print(" - Processos localizados: 1")
                qtd_graus = 1
            elif "2 processos encontrados" in qtd_processos:
                print(" - Processos localizados: 2")
                qtd_graus = 2
            else:
                print(" - Processos localizados: Texto não encontrado com a quantidade de processos ou valor inesperado")    
                problemas = problemas + 1
                qtd_graus = 0

            for qtd in range(1, qtd_graus + 1):
                print(" - Acessando Grau: " + str(qtd))
                
                try:
                    botao_grau = botao_pesquisar = navegador.find_element(By.XPATH, f"/html/body/pje-root/main/pje-lista-processo/div[1]/button[{qtd}]")                                                                                             
                    botao_grau.click()

                    time.sleep(2)

                    captcha(navegador)

                    troca_aba(navegador, janela_original)

                    navegador.close()

                    navegador.switch_to.window(janela_original)

                    navegador.find_element(By.XPATH, '/html/body/pje-root/div[1]/pje-painel-cabecalho/nav/div[1]/a/span').click()

                    inserir_processo(navegador, processo)
                    
                except NoSuchElementException:
                    navegador.quit()

            
            navegador.quit()
                               

        except NoSuchElementException:

            try:
                navegador.find_element(By.XPATH, '//*[@id="painelCaptcha"]')
                captcha(navegador)
            except NoSuchElementException:
                print(" - Entrou no captcha e não localizou o elemento")
                problemas = problemas + 1
            
        except ElementClickInterceptedException:
            print(" - Não foi possível clicar no botão")
            problemas = problemas + 1

        finally:
            # Fecha o WebDriver
            navegador.quit()
        
        if indice == 100:
            print("-----------------------------------")
            print("- Atividade finalizada com sucesso.")
            print("- Sucesso: " + str(sucesso))
            print("- Erro: " + str(problemas))
            print("- Total: " + str(total))
            print("-----------------------------------")
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

    caminho_destino = r"C:\Users\prvf56\OneDrive - PREVI\Projetos\Projeto Ajur\ajur\captcha.jpg"
    
    
    with open(caminho_destino, "wb") as arquivo:
        arquivo.write(image_bytes)

    #print(f"Imagem salva em {caminho_destino}")

    captcha_text = solver.solve_and_return_solution("captcha.jpg")

    if captcha_text != 0:
        print(" - Texto Captcha: "+captcha_text)
        navegador.find_element(By.ID, "captchaInput").send_keys(captcha_text)
        navegador.find_element(By.ID, "btnEnviar").click()
        time.sleep(1)
        navegador.find_element(By.ID, "btnDownloadIntegra").click()
        time.sleep(7)
        print(" - Processo salvo com sucesso.")
        sucesso = sucesso + 1

    else:
        print(" - Tarefa Captcha Finalizou com erro: "+solver.error_code)
        problemas = problemas + 1

    try:
        if os.path.exists(caminho_destino):
            os.remove(caminho_destino)
            print(f" - Arquivo captcha deletado com sucesso!")
        else:
            print(f" - Arquivo captcha não encontrado.")
    except FileNotFoundError:
        print(f"O arquivo '{caminho_destino}' não foi encontrado.")
    except PermissionError:
        print(f"Você não tem permissão para deletar o arquivo '{caminho_destino}'.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {str(e)}")


def troca_aba(navegador, janela_original):
    for window_handle in navegador.window_handles:
        if window_handle != janela_original:
            navegador.switch_to.window(window_handle)
            break

def inserir_processo(navegador, processo):
    aguardar = WebDriverWait(navegador, 100)
    input_numero_processo = aguardar.until(EC.presence_of_element_located((By.ID, "nrProcessoInput")))
    input_numero_processo.send_keys(processo)
    botao_pesquisar = navegador.find_element(By.ID, "btnPesquisar")
    botao_pesquisar.click()
    time.sleep(2)


if __name__ == "__main__":
    main()