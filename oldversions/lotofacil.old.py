# CÓDIGO PARA BAIXAR OS ÚLTIMOS 30 CONCURSOS DA LOTOFÁCIL #
import requests
import sqlite3

# URL base da API para obter resultados
API_URL_BASE = "https://loteriascaixa-api.herokuapp.com/api/lotofacil"

# Função para criar/abrir o banco de dados SQLite e configurar a tabela
def configurar_banco():
    conn = sqlite3.connect("lotofacil.db")  # Cria/abre o arquivo do banco
    cursor = conn.cursor()

    # Cria a tabela para armazenar os resultados, caso ainda não exista
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS resultados (
        concurso INTEGER PRIMARY KEY,
        data TEXT,
        dezenas TEXT
    )
    ''')
    conn.commit()
    return conn

# Função para buscar os resultados de um concurso específico
def obter_resultado_concurso(concurso):
    try:
        url = f"{API_URL_BASE}/{concurso}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro ao obter concurso {concurso}: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
        return None

# Função para salvar um resultado no banco de dados
def salvar_resultado(conn, resultado):
    cursor = conn.cursor()

    # Insere os dados, mas evita duplicação usando o concurso como chave primária
    try:
        cursor.execute('''
        INSERT INTO resultados (concurso, data, dezenas)
        VALUES (?, ?, ?)
        ''', (resultado["concurso"], resultado["data"], ",".join(resultado["dezenas"])))

        conn.commit()
        print(f"Concurso {resultado['concurso']} salvo com sucesso!")
    except sqlite3.IntegrityError:
        print(f"Concurso {resultado['concurso']} já existe no banco de dados.")

# Função para buscar os 30 últimos concursos
def obter_ultimos_concursos(conn, quantidade=30):
    # Primeiro, obtenha o número do último concurso
    try:
        response = requests.get(f"{API_URL_BASE}/latest")
        if response.status_code == 200:
            ultimo_concurso = response.json()["concurso"]
            print(f"Último concurso: {ultimo_concurso}")

            # Loop para buscar os últimos 'quantidade' concursos
            for concurso in range(ultimo_concurso, ultimo_concurso - quantidade, -1):
                print(f"Buscando concurso {concurso}...")
                resultado = obter_resultado_concurso(concurso)
                if resultado:
                    salvar_resultado(conn, resultado)

        else:
            print(f"Erro ao obter o último concurso: {response.status_code}")
    except requests.RequestException as e:
        print(f"Erro ao acessar a API: {e}")

# Função principal para executar o fluxo
def main():
    conn = configurar_banco()  # Configura o banco de dados

    # Obtém e salva os 30 últimos concursos
    obter_ultimos_concursos(conn, quantidade=30)

    conn.close()

if __name__ == "__main__":
    main()


# import requests
# import sqlite3
# import time


# # URL da API para obter resultados da Lotofácil
# API_URL = "https://loteriascaixa-api.herokuapp.com/api/lotofacil/latest"
# # response = requests.get(url, verify=False)
# # print(response.json())

# # Função para criar/abrir o banco de dados SQLite e configurar a tabela
# def configurar_banco():
#     conn = sqlite3.connect("lotofacil.db")  # Cria/abre o arquivo do banco
#     cursor = conn.cursor()

#     # Cria a tabela para armazenar os resultados, caso ainda não exista
#     cursor.execute('''
#     CREATE TABLE IF NOT EXISTS resultados (
#         concurso INTEGER PRIMARY KEY,
#         data TEXT,
#         dezenas TEXT
#     )
#     ''')
#     conn.commit()
#     return conn

# # Função para buscar os resultados da API
# def obter_resultados():
#     try:
#         response = requests.get(API_URL)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             print(f"Erro na API: {response.status_code}")
#             return None
#     except requests.RequestException as e:
#         print(f"Erro ao acessar a API: {e}")
#         return None

# # Função para salvar os resultados no banco de dados
# def salvar_resultado(conn, resultado):
#     cursor = conn.cursor()

#     # Insere os dados, mas evita duplicação usando o concurso como chave primária
#     try:
#         cursor.execute('''
#         INSERT INTO resultados (concurso, data, dezenas)
#         VALUES (?, ?, ?)
#         ''', (resultado["concurso"], resultado["data"], ",".join(resultado["dezenas"])))

#         conn.commit()
#         print(f"Concurso {resultado['concurso']} salvo com sucesso!")
#     except sqlite3.IntegrityError:
#         print(f"Concurso {resultado['concurso']} já existe no banco de dados.")

# # Função principal para integrar os passos
# def main():
#     conn = configurar_banco()

#     while True:  # Loop infinito para buscar atualizações automaticamente
#         resultado = obter_resultados()

#         if resultado:
#             salvar_resultado(conn, resultado)

#         print("Aguardando o próximo ciclo...")
#         time.sleep(3600)  # Espera 1 hora antes de verificar novamente (pode ajustar o intervalo)

#     conn.close()

# if __name__ == "__main__":
#     main()


