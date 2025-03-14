import sqlite3
import requests

# Configuração do banco de dados SQLite
DB_NAME = "lotofacil.db"

def criar_tabela():
    """Cria a tabela no banco de dados se não existir."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lotofacil (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            concurso INTEGER UNIQUE,
            data_apuracao TEXT,
            dezenas TEXT,
            acumulado INTEGER
        )
    """)
    conn.commit()
    conn.close()

def obter_dados_concurso(numero_concurso):
    """Obtém os dados de um concurso específico."""
    url = f"https://servicebus2.caixa.gov.br/portaldeloterias/api/lotofacil/{numero_concurso}"
    try:
        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()
        return resposta.json()
    except requests.RequestException as e:
        print(f"Erro ao acessar {url}: {e}")
        return None

def salvar_concurso(concurso, data_apuracao, dezenas, acumulado):
    """Salva os dados do concurso no banco de dados, se ainda não estiver salvo."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Verificar se o concurso já existe no banco
    cursor.execute("SELECT 1 FROM lotofacil WHERE concurso = ?", (concurso,))
    if cursor.fetchone():
        print(f"Concurso {concurso} já está salvo no banco de dados.")
    else:
        # Inserir o concurso no banco de dados caso ainda não exista
        cursor.execute("""
            INSERT INTO lotofacil (concurso, data_apuracao, dezenas, acumulado)
            VALUES (?, ?, ?, ?)
        """, (concurso, data_apuracao, ",".join(dezenas), int(acumulado)))
        conn.commit()
        print(f"Concurso {concurso} salvo com sucesso.")

    conn.close()


def obter_ultimo_concurso():
    """Obtém o número do último concurso disponível na API."""
    dados = obter_dados_concurso("")
    if dados:
        return dados.get("numero")
    return None

def buscar_ultimos_concursos(qtd=50):
    """Busca e salva os últimos 'qtd' concursos no banco."""
    criar_tabela()
    ultimo_concurso = obter_ultimo_concurso()

    if not ultimo_concurso:
        print("Não foi possível obter o último concurso.")
        return

    for numero in range(ultimo_concurso, ultimo_concurso - qtd, -1):
        dados = obter_dados_concurso(numero)
        if dados:
            salvar_concurso(
                dados["numero"],
                dados["dataApuracao"],
                dados["listaDezenas"],
                dados["acumulado"]
            )
            print(f"Concurso {dados['numero']} salvo.")
        else:
            print(f"Falha ao obter dados do concurso {numero}.")

if __name__ == "__main__":
    buscar_ultimos_concursos()
