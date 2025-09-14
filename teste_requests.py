import requests
import json

# URL do seu endpoint Flask
URL_ENDPOINT = "http://127.0.0.1:5000/exibir-conteudo"

# Dados que você quer enviar no corpo da requisição
# O nome da chave 'conteudo' deve ser exatamente o que o seu endpoint espera
dados = {
    "conteudo": "Olá do arquivo Python! Enviando uma mensagem para o endpoint."
}

try:
    # Envia uma requisição POST com o JSON no corpo.
    # O parâmetro 'json' cuida de converter o dicionário Python para JSON.
    response = requests.post(URL_ENDPOINT, json=dados)

    # Verifica se a requisição foi bem-sucedida (código 200)
    if response.status_code == 200:
        print("Requisição bem-sucedida!")
        print("O sino da igrejinha faz..")
        print(response.text)
    else:
        print(f"Erro na requisição. Código de status: {response.status_code}")
        print(response.text)

except requests.exceptions.RequestException as e:
    # Captura possíveis erros de conexão (servidor fora do ar, URL incorreta, etc.)
    print(f"Ocorreu um erro ao conectar ao servidor: {e}")