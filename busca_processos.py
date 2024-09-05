import time
import base64
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from anticaptchaofficial.imagecaptcha import *
from PIL import Image
from io import BytesIO



solver = imagecaptcha()
solver.set_verbose(1)
solver.set_key("bac6d8977d6fa8fab6b9530243eb2544")

solver.set_soft_id(0)


url = 'https://pje.trt5.jus.br/consultaprocessual/'
processo = '0000966-54.2016.5.05.0222'

navegador = webdriver.Firefox()
navegador.get(url)

aguardar = WebDriverWait(navegador, 100)
input_numero_processo = aguardar.until(EC.presence_of_element_located((By.ID, "nrProcessoInput")))
input_numero_processo.send_keys(processo)

botao_pesquisar = navegador.find_element(By.ID, "btnPesquisar")
botao_pesquisar.click()

time.sleep(2)
botao_primeiro_grau = botao_pesquisar = navegador.find_element(By.XPATH, "/html/body/pje-root/main/pje-lista-processo/div[1]/button[1]")
botao_primeiro_grau.click()

time.sleep(2)
img = navegador.find_element(By.ID, "imagemCaptcha")
base64_string = img.get_attribute('src')

imagem = base64_string.split(",", 1)

image_bytes = base64.b64decode(imagem[1])

caminho_destino = r"D:\Projetos\Ajur\processos\captcha.jpg"

with open(caminho_destino, "wb") as arquivo:
    arquivo.write(image_bytes)

print(f"Imagem salva em {caminho_destino}")

captcha_text = solver.solve_and_return_solution("captcha.jpg")
if captcha_text != 0:
    print("captcha text "+captcha_text)
else:
    print("task finished with error "+solver.error_code)