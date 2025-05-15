from selenium import webdriver                            # Importa o módulo webdriver do Selenium, que permite controlar o browser via código
from selenium.webdriver.chrome.service import Service    # Importa a classe Service, usada para especificar o executável do ChromeDriver
from webdriver_manager.chrome import ChromeDriverManager  # Importa o gerenciador automático de versão do ChromeDriver
from selenium.webdriver.common.by import By               # Importa o enum By, que ajuda a localizar elementos (ID, XPATH, CSS etc.)
import time                                               # Importa o módulo time para usar sleep() e pausar o script
import os                                                 # Importa o módulo os para manipulação de caminhos e arquivos

# Caminho absoluto para o arquivo HTML de Recife (não usado diretamente, mas ilustrativo)
caminho_html = 'C:/Users/cleyb/Documents/ecotour/pages/recife.html'

# Caminho absoluto para a página inicial (index.html)
url_home = 'C:/Users/cleyb/Documents/ecotour/index.html'

# Inicia o Chrome, instalando/configurando automaticamente o ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Abre a página inicial local no navegador
driver.get(url_home)

# --- NAVEGAÇÃO PARA RECIFE ---
time.sleep(3)  # Espera 3 segundos para garantir que a página carregou
botao_recife = driver.find_element(
    By.XPATH,
    "//h3[contains(text(), 'Recife')]/following-sibling::a[contains(@class, 'btn')]"
)  # Localiza o botão "Saiba mais" de Recife via XPath
botao_recife.click()  # Clica no botão de Recife
time.sleep(3)  # Espera o carregamento da nova página
# Verifica se a URL atual contém 'recife.html' e imprime resultado
if 'recife.html' in driver.current_url:
    print("Navegação para a página de Recife bem-sucedida!")
else:
    print(f"Falha na navegação. URL atual: {driver.current_url}")

# --- FUNÇÕES DE ROLAGEM ---

def rolar_suavemente(driver, destino='fim', pixels=None):
    """
    Rola a página de forma suave.
    Se destino=='fim', rola até o fim da página.
    Se pixels for número, rola até essa quantidade de pixels.
    """
    if destino == 'fim':
        altura_total = driver.execute_script("return document.body.scrollHeight")
        altura_atual = 0
        while altura_atual < altura_total:
            altura_atual += 30
            driver.execute_script(f"window.scrollTo(0, {altura_atual});")
            time.sleep(0.8)
    elif pixels:
        altura_atual = 0
        while altura_atual < pixels:
            altura_atual += 40
            driver.execute_script(f"window.scrollTo(0, {altura_atual});")
            time.sleep(0.3)

def rolar_ate_elemento(driver, elemento):
    """
    Rola a página até que o elemento especificado esteja visível na viewport.
    """
    posicao = elemento.location['y']                             # Pega a coordenada Y do elemento
    altura_atual = driver.execute_script("return window.pageYOffset")  # Posição atual da rolagem
    while altura_atual < posicao:
        altura_atual += 40                                        # Incremento de 40px por vez
        driver.execute_script(f"window.scrollTo(0, {altura_atual});")
        time.sleep(0.3)

# --- PREENCHIMENTO DO FORMULÁRIO DE RECIFE ---

# Localiza o campo "nome" pelo ID
nome_input = driver.find_element(By.ID, "name")
rolar_ate_elemento(driver, nome_input)  # Rola até o campo de nome
time.sleep(2)                            # Espera para animar/garantir visibilidade
try:
    nome_input.send_keys("José PlayTV")  # Digita "José PlayTV" no campo nome
    print("Campo nome preenchido com sucesso!")
except Exception as e:
    print(f"Erro ao preencher o campo nome: {str(e)}")
time.sleep(2)

# Localiza o campo "email" pelo ID e preenche
try:
    email_input = driver.find_element(By.ID, "email")
    rolar_ate_elemento(driver, email_input)
    time.sleep(2)
    email_input.send_keys("jose.playtv@email.com")
    print("Campo email preenchido com sucesso!")
except Exception as e:
    print(f"Erro ao preencher o campo email: {str(e)}")
time.sleep(2)

# Seleciona 4 estrelas na avaliação via JavaScript
try:
    driver.execute_script("""
        var stars = document.querySelectorAll('.star-rating input[type="radio"]');
        if (stars.length > 1) {
            stars[1].click();    // Clica no segundo input (star4)
            stars[1].checked = true;
        }
    """)
    print("Avaliação selecionada com sucesso!")
except Exception as e:
    print(f"Erro ao selecionar a avaliação: {str(e)}")
time.sleep(2)

# Upload de imagem para Recife
try:
    # Monta o caminho absoluto da imagem em relação a este script
    imagem_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "./images/imagem_recife.jpg")
    if not os.path.exists(imagem_path):
        print(f"Arquivo não encontrado: {imagem_path}")
        with open(imagem_path, 'w') as f:
            f.write('')  # Cria arquivo vazio como fallback
    file_input = driver.find_element(By.ID, "media")  # Localiza o input de arquivo
    file_input.send_keys(imagem_path)                 # Envia o arquivo para upload
    print("Arquivo enviado com sucesso!")
except Exception as e:
    print(f"Erro ao enviar o arquivo: {str(e)}")
time.sleep(2)

# Preenche o comentário
try:
    comment_input = driver.find_element(By.ID, "comment")
    rolar_ate_elemento(driver, comment_input)
    time.sleep(2)
    comment_input.send_keys(
        "Recife é uma cidade incrível! A arquitetura histórica, as praias e a culinária local são fantásticas. "
        "Recomendo muito a visita ao Marco Zero e ao Recife Antigo."
    )
    print("Comentário preenchido com sucesso!")
except Exception as e:
    print(f"Erro ao preencher o comentário: {str(e)}")

# Clica no botão de submit para enviar o formulário
submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
submit_button.click()
time.sleep(3)

# Clica no link "Home" para voltar à página inicial
home_link = driver.find_element(By.XPATH, "//a[text()='Home']")
home_link.click()
time.sleep(3)

# Verifica se voltou para 'index.html'
if 'index.html' in driver.current_url:
    print("Retorno para a página inicial bem-sucedido!")
else:
    print(f"Falha ao retornar para a página inicial. URL atual: {driver.current_url}")

time.sleep(3)

# --- FLUXO PARA NATAL (mesma lógica de Recife, mas com dados de Natal) ---
try:
    botao_natal = driver.find_element(
        By.XPATH,
        "//h3[contains(text(), 'Natal')]/following-sibling::a[contains(@class, 'btn')]"
    )
    botao_natal.click()
    time.sleep(3)
    if 'natal.html' in driver.current_url:
        print("Navegação para a página de Natal bem-sucedida!")
    else:
        print(f"Falha na navegação para Natal. URL atual: {driver.current_url}")

    # Preenchimento de nome e email
    nome_input = driver.find_element(By.ID, "name")
    rolar_ate_elemento(driver, nome_input)
    nome_input.send_keys("Maria Souza")
    time.sleep(2)

    email_input = driver.find_element(By.ID, "email")
    rolar_ate_elemento(driver, email_input)
    email_input.send_keys("maria.souza@email.com")
    time.sleep(2)

    # Seleciona 3 estrelas (star3)
    driver.execute_script("""
        var stars = document.querySelectorAll('.star-rating input[type="radio"]');
        if (stars.length > 2) {
            stars[2].click();
            stars[2].checked = true;
        }
    """)
    time.sleep(2)

    # Upload de imagem para Natal
    imagem_path_natal = os.path.join(os.path.dirname(os.path.abspath(__file__)), "./images/imagem_natal.jpg")
    if not os.path.exists(imagem_path_natal):
        print(f"Arquivo não encontrado: {imagem_path_natal}")
        with open(imagem_path_natal, 'w') as f:
            f.write('')
    file_input = driver.find_element(By.ID, "media")
    file_input.send_keys(imagem_path_natal)
    time.sleep(2)

    # Comentário para Natal
    comment_input = driver.find_element(By.ID, "comment")
    rolar_ate_elemento(driver, comment_input)
    comment_input.send_keys(
        "Natal é maravilhosa! As dunas e praias são espetaculares. Passeio de buggy imperdível!"
    )
    time.sleep(4)

    # Envio e retorno ao Home
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()
    time.sleep(3)
    home_link = driver.find_element(By.XPATH, "//a[text()='Home']")
    home_link.click()
    time.sleep(3)

    if 'index.html' in driver.current_url:
        print("Retorno para a página inicial após Natal bem-sucedido!")
    else:
        print(f"Falha ao retornar após Natal. URL atual: {driver.current_url}")
except Exception as e:
    print(f"Erro no fluxo de Natal: {str(e)}")

# --- FLUXO PARA SALVADOR (mesma lógica com dados de Salvador) ---
try:
    botao_salvador = driver.find_element(
        By.XPATH,
        "//h3[contains(text(), 'Salvador')]/following-sibling::a[contains(@class, 'btn')]"
    )
    botao_salvador.click()
    time.sleep(3)

    if 'salvador.html' in driver.current_url:
        print("Navegação para a página de Salvador bem-sucedida!")
    else:
        print(f"Falha na navegação para Salvador. URL atual: {driver.current_url}")

    nome_input = driver.find_element(By.ID, "name")
    rolar_ate_elemento(driver, nome_input)
    time.sleep(2)
    nome_input.send_keys("Carlos Oliveira")

    email_input = driver.find_element(By.ID, "email")
    rolar_ate_elemento(driver, email_input)
    time.sleep(2)
    email_input.send_keys("carlos.oliveira@email.com")

    # Seleciona 1 estrela (star1) — o quinto input
    driver.execute_script("""
        var stars = document.querySelectorAll('.star-rating input[type="radio"]');
        if (stars.length > 4) {
            stars[4].click();
            stars[4].checked = true;
        }
    """)
    time.sleep(2)

    # Upload de imagem para Salvador
    imagem_path_salvador = os.path.join(os.path.dirname(os.path.abspath(__file__)), "./images/imagem_salvador.jpg")
    if not os.path.exists(imagem_path_salvador):
        print(f"Arquivo não encontrado: {imagem_path_salvador}")
        with open(imagem_path_salvador, 'w') as f:
            f.write('')
    file_input = driver.find_element(By.ID, "media")
    file_input.send_keys(imagem_path_salvador)
    time.sleep(2)

    # Comentário para Salvador
    comment_input = driver.find_element(By.ID, "comment")
    rolar_ate_elemento(driver, comment_input)
    time.sleep(2)
    comment_input.send_keys(
        "Salvador tem uma energia única! Cultura, música e praias incríveis. Recomendo o Pelourinho!"
    )
    time.sleep(4)

    # Envia e retorna ao home
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()
    time.sleep(3)
    home_link = driver.find_element(By.XPATH, "//a[text()='Home']")
    home_link.click()
    time.sleep(3)

    if 'index.html' in driver.current_url:
        print("Retorno para a página inicial após Salvador bem-sucedido!")
    else:
        print(f"Falha ao retornar após Salvador. URL atual: {driver.current_url}")
except Exception as e:
    print(f"Erro no fluxo de Salvador: {str(e)}")

# Fecha o navegador e encerra o WebDriver
driver.quit()
