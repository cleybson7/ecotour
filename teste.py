from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import os

# Caminho absoluto para o arquivo HTML
caminho_html = 'C:/Users/cleyb/Documents/ecotour/pages/recife.html'

url_home = 'C:/Users/cleyb/Documents/ecotour/index.html'
# Iniciar o Chrome 
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Abrir o HTML local
driver.get(url_home)

# Encontrar e clicar no botão 'Saiba mais' de Recife
time.sleep(3)  # Aguardar carregamento da página
botao_recife = driver.find_element(By.XPATH, "//h3[contains(text(), 'Recife')]/following-sibling::a[contains(@class, 'btn')]")
botao_recife.click()

# Verificar se a navegação foi bem-sucedida
time.sleep(3)  # Aguardar carregamento da nova página
if 'recife.html' in driver.current_url:
    print("Navegação para a página de Recife bem-sucedida!")
else:
    print(f"Falha na navegação. URL atual: {driver.current_url}")

# Função para rolagem suave
def rolar_suavemente(driver, destino='fim', pixels=None):
    if destino == 'fim':
        altura_total = driver.execute_script("return document.body.scrollHeight")
        altura_atual = 0
        while altura_atual < altura_total:
            altura_atual += 30  # Reduzido ainda mais para movimento mais suave
            driver.execute_script(f"window.scrollTo(0, {altura_atual});")
            time.sleep(0.8)  # Aumentado para movimento mais lento na página inicial
    elif pixels:
        altura_atual = 0
        while altura_atual < pixels:
            altura_atual += 40  # Aumentado para movimento mais rápido
            driver.execute_script(f"window.scrollTo(0, {altura_atual});")
            time.sleep(0.3)  # Reduzido para movimento mais rápido na página de destino

def rolar_ate_elemento(driver, elemento):
    # Obtém a posição do elemento e a posição atual da rolagem
    posicao = elemento.location['y']
    altura_atual = driver.execute_script("return window.pageYOffset")
    # Rola suavemente até o elemento a partir da posição atual
    while altura_atual < posicao:
        altura_atual += 40
        driver.execute_script(f"window.scrollTo(0, {altura_atual});")
        time.sleep(0.3)

# Localizar o primeiro campo do formulário (nome)
nome_input = driver.find_element(By.ID, "name")

# Rolar diretamente para o primeiro campo
rolar_ate_elemento(driver, nome_input)
time.sleep(2)

# Preencher o campo nome
try:
    nome_input.send_keys("João Silva")
    print("Campo nome preenchido com sucesso!")
except Exception as e:
    print(f"Erro ao preencher o campo nome: {str(e)}")

time.sleep(2)

# Preencher o campo email
try:
    email_input = driver.find_element(By.ID, "email")
    rolar_ate_elemento(driver, email_input)
    time.sleep(2)
    email_input.send_keys("joao.silva@email.com")
    print("Campo email preenchido com sucesso!")
except Exception as e:
    print(f"Erro ao preencher o campo email: {str(e)}")

time.sleep(2)

# Selecionar avaliação
try:
    # Usar JavaScript para clicar no radio button de 4 estrelas
    # Os inputs são listados na ordem: star5, star4, star3, star2, star1
    # Para selecionar 4 estrelas (id="star4"), é o segundo elemento (índice 1)
    driver.execute_script("""
        var stars = document.querySelectorAll('.star-rating input[type="radio"]');
        if (stars.length > 1) { // star4 é o segundo elemento
            stars[1].click(); // Clica em star4
            stars[1].checked = true;
        }
    """)
    print("Avaliação selecionada com sucesso!")
except Exception as e:
    print(f"Erro ao selecionar a avaliação: {str(e)}")

time.sleep(2)

# Upload de arquivo
try:
    # Criar caminho absoluto para a imagem no diretório do projeto
    imagem_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imagem_recife.jpg")
    
    # Verificar se o arquivo existe
    if not os.path.exists(imagem_path):
        print(f"Arquivo não encontrado: {imagem_path}")
        # Criar um arquivo de texto vazio como fallback
        with open(imagem_path, 'w') as f:
            f.write('')
    
    # Localizar e interagir com o elemento de upload
    file_input = driver.find_element(By.ID, "media") # Corrigido o ID para 'media'
    # O input de arquivo já é visível ou não precisa ser tornado visível para send_keys funcionar em muitos casos
    # Se ainda houver problemas, a linha abaixo pode ser descomentada:
    # driver.execute_script("arguments[0].style.display = 'block'; arguments[0].style.visibility = 'visible'; arguments[0].style.height = '1px'; arguments[0].style.width = '1px'; arguments[0].style.opacity = 1;", file_input)
    file_input.send_keys(imagem_path)
    print("Arquivo enviado com sucesso!")
except Exception as e:
    print(f"Erro ao enviar o arquivo: {str(e)}")

time.sleep(2)

# Preencher comentário
try:
    comment_input = driver.find_element(By.ID, "comment")
    rolar_ate_elemento(driver, comment_input)
    time.sleep(2)
    comment_input.send_keys("Recife é uma cidade incrível! A arquitetura histórica, as praias e a culinária local são fantásticas. Recomendo muito a visita ao Marco Zero e ao Recife Antigo.")
    print("Comentário preenchido com sucesso!")
except Exception as e:
    print(f"Erro ao preencher o comentário: {str(e)}")

# Clicar no botão de enviar
submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
submit_button.click()

time.sleep(3)  # Aguardar o processamento do formulário

# Clicar no link Home para voltar à página principal
home_link = driver.find_element(By.XPATH, "//a[text()='Home']")
home_link.click()

time.sleep(3)  # Aguardar o carregamento da página inicial

# Verificar se voltou para a página inicial
if 'index.html' in driver.current_url:
    print("Retorno para a página inicial bem-sucedido!")
else:
    print(f"Falha ao retornar para a página inicial. URL atual: {driver.current_url}")

# Formas de encontrar o elemento html
'''
usuario = driver.find_element(By.ID, "usuario")
#driver.find_element(By.NAME, "usuario")
#driver.find_element(By.TAG_NAME, "input")
#driver.find_element(By.CSS_SELECTOR, "#usuario")  
senha = driver.find_element(By.ID, "senha")

h1 = driver.find_element(By.TAG_NAME, "h1").text
if h1 == "Login":
    print("H1 tem escrito login")
else:
    print (f'H1 TEM ESCRITO {h1}')
'''
time.sleep(3)

'''
#funções do selenium
time.sleep(1)
# Digita o nome de usuário
usuario.send_keys("admin")
# Digita a senha
senha.send_keys("123")
time.sleep(3)
# Limpa o campo de usuário
usuario.clear()
# Digita novamente
usuario.send_keys("Pamella")
# Clica no botão de login
driver.find_element(By.ID, "btnLogin").click()


# driver.current_url retorna a url
if driver.current_url == url_home:
    print("Redirecionamento bem-sucedido!")
else:
    print(f"Redirecionamento falhou. URL atual: {driver.current_url}")

time.sleep(5)


# Verifica se a página carregou e encontra a caixa de seleção pelo ID
checkbox = driver.find_element(By.ID, "aceite")

# Verifica o estado da caixa de seleção (se está desmarcada inicialmente)
if not checkbox.is_selected():
    print("A caixa de seleção não está marcada inicialmente. Marcando agora...")
    checkbox.click()  # Marca a caixa de seleção

# Verifica se a caixa foi marcada com sucesso
if checkbox.is_selected():
    print("A caixa de seleção foi marcada com sucesso!")
else:
    print("Falha ao marcar a caixa de seleção.")
   
   

# Encontrar todas as caixas de seleção pelo nome
checkboxes = driver.find_elements(By.NAME, "interesses")

# Marcar todas as caixas de seleção
for checkbox in checkboxes:
    if not checkbox.is_selected():
        checkbox.click()

# Verificar se todas as caixas de seleção estão marcadas
for checkbox in checkboxes:
    assert checkbox.is_selected(), "Uma das caixas de seleção não foi marcada."

    
time.sleep(3)
 

usuarios = [
    {"usuario": "admin", "senha": "123"},
    {"usuario": "user1", "senha": "senhaerrada"},
    {"usuario": "user2", "senha": "123"},
    {"usuario": "user3", "senha": ""}
]

for user in usuarios:
    usuario.send_keys(user["usuario"])
    senha.send_keys(user["senha"])
    time.sleep(2)
    usuario.clear()
    senha.clear()

driver.find_element(By.ID, "btnLogin").click()
time.sleep(2)
    # Aqui você pode verificar a URL ou mensagem de erro conforme necessário
if 'home.html' in driver.current_url:
        print(f"Login bem-sucedido para {user['usuario']}")
else:
        print(f"Erro no login para {user['usuario']}")
'''

# Fechar o navegador
driver.quit()