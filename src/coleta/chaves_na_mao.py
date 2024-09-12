import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Inicializa o WebDriver
driver = webdriver.Chrome()

# URL da página
url = "https://www.chavesnamao.com.br/imoveis-para-alugar/sp-sao-paulo/"
driver.get(url)

# Caminho para salvar o arquivo
file_path = "E:/projeto_scraping_chaves_na_mao/src/data/imoveis.jsonl"

# Função para salvar os dados no formato JSONL
def salvar_dados_jsonl(dados, file_path):
    with open(file_path, 'a', encoding='utf-8') as f:
        for dado in dados:
            f.write(json.dumps(dado, ensure_ascii=False) + '\n')

# Função para coletar os dados da página
def coletar_dados():
    imoveis = []
    elementos_imoveis = driver.find_elements(By.CLASS_NAME, "imoveis__Card-obm8pe-0")
    
    for elemento in elementos_imoveis:
        try:
            descricao = elemento.find_element(By.TAG_NAME, "h2").text
            endereco = elemento.find_element(By.CSS_SELECTOR, "address small").text
            bairro = elemento.find_element(By.CSS_SELECTOR, "address b").text
            #aluguel = elemento.find_element(By.CLASS_NAME, "price").text
            aluguel = elemento.find_element(By.CLASS_NAME, "price").text.split("\n")[0].strip()

            
            # Capturando o valor de metros quadrados
            try:
                area_m2 = elemento.find_element(By.XPATH, ".//li[contains(text(),'m²')]").text
            except:
                area_m2 = None

            # Usando XPath para pegar quartos, banheiros e garagens
            try:
                quartos = elemento.find_element(By.XPATH, ".//li[contains(., 'Quartos')]").text
            except:
                quartos = None
            
            try:
                banheiros = elemento.find_element(By.XPATH, ".//li[contains(., 'Banheiros')]").text
            except:
                banheiros = None
            
            try:
                garagens = elemento.find_element(By.XPATH, ".//li[contains(., 'Garagens')]").text
            except:
                garagens = None

            condominio = elemento.find_element(By.CLASS_NAME, "cond").text if elemento.find_elements(By.CLASS_NAME, "cond") else None

            # Verificar no console os detalhes antes de salvar
            print(f"Descrição: {descricao}, Quartos: {quartos}, Banheiros: {banheiros}, Garagens: {garagens}")
            
            imovel = {
                "descricao": descricao,
                "endereco": endereco,
                "bairro": bairro,
                "area_m2": area_m2,
                "quartos": quartos,
                "banheiros": banheiros,
                "garagens": garagens,
                "aluguel": aluguel,
                "condominio": condominio
            }
            imoveis.append(imovel)
        except Exception as e:
            print(f"Erro ao coletar dados: {e}")
    return imoveis

# Função para rolar a página até carregar mais resultados
def rolar_pagina():
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(3)

# Loop principal
ultima_altura = driver.execute_script("return document.body.scrollHeight")
while True:
    # Rola a página para carregar mais resultados
    rolar_pagina()
    
    # Coleta os dados da página atual
    dados_coletados = coletar_dados()
    
    # Salva os dados no arquivo JSONL
    salvar_dados_jsonl(dados_coletados, file_path)
    
    # Verifica se a página continua carregando novos elementos
    nova_altura = driver.execute_script("return document.body.scrollHeight")
    if nova_altura == ultima_altura:
        print("Fim da página ou sem novos dados para carregar.")
        break
    ultima_altura = nova_altura

# Fechar o navegador ao final
driver.quit()
