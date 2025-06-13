import sqlite3

DATABASE_PATH = "lotofacil.db"

def listar_jogos():
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT concurso, dezenas FROM lotofacil
                ORDER BY concurso ASC
            ''')
            resultados = cursor.fetchall()
            if resultados:
                print("Lista de todos os jogos salvos no banco de dados:\n")
                for concurso, dezenas in resultados:
                    dezenas_formatadas = " ".join(f"{int(num):02d}" for num in dezenas.split(","))
                    print(f"Concurso {concurso}: {dezenas_formatadas}")
                print(f"\nTotal de jogos salvos: {len(resultados)}")
            else:
                print("Nenhum jogo encontrado no banco de dados.")
    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")

if __name__ == "__main__":
    listar_jogos()