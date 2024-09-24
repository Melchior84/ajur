import time
import base64
import os
import pandas as pd
import shutil
import logging

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
    logging.basicConfig(filename='AsJur.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    grava_log("-----------------------------------", 'I')
    grava_log("  RPA Baixar Processos para AJUR   ", 'I')
    grava_log("-----------------------------------", 'I')

    global total 
    global sucesso
    global problemas

    arquivo = r"C:\Users\prvf56\OneDrive - PREVI\Projetos\Projeto Ajur\ajur\processos.xlsx"
    dados = pd.read_excel(arquivo)
    totalLinhas = dados.shape[0]
    qtd_graus = 0

    grava_log("-----------------------------------", 'I')
    grava_log('Total de linhas do arquivo: ' + str(totalLinhas), 'I') 
    grava_log("-----------------------------------", 'I')

    for indice, linha in dados[21:].iterrows():
        grava_log(f'Registro ({indice}) - {linha['Matrícula']} - {linha['processo']} - {linha['Nome']} - {linha['site']}', 'I')
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
                grava_log(" - Processos localizados: 0", 'I')
                qtd_graus = 0
                problemas = problemas + 1
            elif "1 processos encontrados" in qtd_processos:
                grava_log(" - Processos localizados: 1", 'I')
                qtd_graus = 1
            elif "2 processos encontrados" in qtd_processos:
                grava_log(" - Processos localizados: 2", 'I')
                qtd_graus = 2
            else:
                grava_log(" - Processos localizados: Texto não encontrado com a quantidade de processos ou valor inesperado", 'I')    
                problemas = problemas + 1
                qtd_graus = 0

            for qtd in range(1, qtd_graus + 1):
                grava_log(" - Acessando Grau: " + str(qtd), 'I')
                
                try:
                    botao_grau = botao_pesquisar = navegador.find_element(By.XPATH, f"/html/body/pje-root/main/pje-lista-processo/div[1]/button[{qtd}]")                                                                                             
                    botao_grau.click()

                    time.sleep(2)

                    captcha(navegador)

                    renomear_arquivo(linha['Nome'], linha['processo'], qtd)

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
                renomear_arquivo(linha['Nome'], linha['processo'], 1)
            except NoSuchElementException:
                grava_log(" - Entrou no captcha e não localizou o elemento", 'W')
                problemas = problemas + 1
            
        except ElementClickInterceptedException:
            grava_log(" - Não foi possível clicar no botão", 'W')
            problemas = problemas + 1

        finally:
            # Fecha o WebDriver
            navegador.quit()
        
        if indice == 100:
            grava_log("-----------------------------------", 'I')
            grava_log("- Atividade finalizada com sucesso.", 'I')
            grava_log("- Sucesso: " + str(sucesso), 'I')
            grava_log("- Erro: " + str(problemas), 'I')
            grava_log("- Total: " + str(total), 'I')
            grava_log("-----------------------------------", 'I')
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
        grava_log(" - Texto Captcha: "+captcha_text, 'I')
        navegador.find_element(By.ID, "captchaInput").send_keys(captcha_text)
        navegador.find_element(By.ID, "btnEnviar").click()
        time.sleep(1)
        navegador.find_element(By.ID, "btnDownloadIntegra").click()
        time.sleep(5)
        grava_log(" - Processo salvo com sucesso.", 'I')
        sucesso = sucesso + 1

    else:
        grava_log(" - Tarefa Captcha Finalizou com erro: "+solver.error_code, 'E')
        problemas = problemas + 1

    try:
        if os.path.exists(caminho_destino):
            os.remove(caminho_destino)
            grava_log(f" - Arquivo captcha deletado com sucesso!", 'I')
        else:
            grava_log(f" - Arquivo captcha não encontrado.", 'E')
    except FileNotFoundError:
        grava_log(f"O arquivo '{caminho_destino}' não foi encontrado.", 'E')
    except PermissionError:
        grava_log(f"Você não tem permissão para deletar o arquivo '{caminho_destino}'.", 'E')
    except Exception as e:
        grava_log(f"Ocorreu um erro inesperado: {str(e)}", 'E')


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

import os
import shutil

def renomear_arquivo(nome, numero_processo, instancia):
    # Diretório de downloads
    downloads_dir = os.path.expanduser('~/Downloads')
    # Diretório de destino
    destino_dir = f'C:/temp/{nome}_{numero_processo}'

    # Listar arquivos PDF no diretório de downloads
    arquivos = [f for f in os.listdir(downloads_dir) if f.endswith('.pdf')]

    # Encontrar o arquivo com o número do processo
    arquivo_encontrado = None
    for arquivo in arquivos:
        if numero_processo in arquivo:
            arquivo_encontrado = arquivo
            break

    if arquivo_encontrado:
        # Criar diretório de destino se não existir
        os.makedirs(destino_dir, exist_ok=True)

        # Novo nome do arquivo com base na instância
        novo_nome = f'{nome}_{numero_processo}_Grau_{instancia}.pdf'
        # Caminho completo do arquivo encontrado e do novo arquivo
        caminho_arquivo_encontrado = os.path.join(downloads_dir, arquivo_encontrado)
        caminho_novo_arquivo = os.path.join(destino_dir, novo_nome)

        # Renomear e mover o arquivo
        shutil.move(caminho_arquivo_encontrado, caminho_novo_arquivo)
        grava_log(f' - Arquivo renomeado e movido.', 'I')
    else:
        grava_log(' - Arquivo não encontrado com o número do processo fornecido.', 'E')

def grava_log(mensagem, tipo):

    if tipo == 'D':
        logging.debug(mensagem)
    elif tipo == 'I':
        logging.info(mensagem)
    elif tipo == 'W':
        logging.warning(mensagem)
    elif tipo == 'E':
        logging.error(mensagem)
    elif tipo == 'C':
        logging.critical(mensagem)
    else:
        logging.info(mensagem)
    
    print(mensagem)



if __name__ == "__main__":
    main()