import os       # Para montar caminhos de arquivo de forma portável
import sqlite3  # Banco de dados SQLite


# ──────────────────────────────────────────────
# CAMADA DE ACESSO AO BANCO DE DADOS
# Gerencia a conexão com o SQLite e todas as operações de leitura/escrita.
# O arquivo .db é criado automaticamente na primeira execução.
# ──────────────────────────────────────────────
class BancoDeDados:

    def __init__(self):
        # Se estiver rodando como executável compilado (PyInstaller),
        # salva o banco de dados na mesma pasta do executável para persistência.
        # Caso contrário (desenvolvimento), salva na pasta data/.
        import sys
        if getattr(sys, 'frozen', False):
            diretorio_base = os.path.dirname(sys.executable)
        else:
            diretorio_base = os.path.dirname(__file__)

        caminho_banco = os.path.join(diretorio_base, "batalhas_pokemon.db")
        self.conexao = sqlite3.connect(caminho_banco)  # Abre (ou cria) o arquivo .db
        self.cursor = self.conexao.cursor()            # Cursor é o objeto que executa SQL
        self.criar_tabelas()                           # Garante que a tabela existe antes de usar

    def criar_tabelas(self):
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS historico
                            (
                                id              INTEGER PRIMARY KEY AUTOINCREMENT, -- ID único gerado automaticamente
                                jogador         TEXT,  -- Nome do treinador
                                pokemon_jogador TEXT,  -- Nome do Pokémon usado pelo jogador
                                pokemon_inimigo TEXT,  -- Nome do Pokémon oponente
                                resultado       TEXT   -- "Vitória" ou "Derrota"
                            )
                            """)
        self.conexao.commit()  # commit() confirma e salva as alterações no arquivo

    def registrar_batalha(self, jogador, pokemon_jogador, pokemon_inimigo, resultado):
        # Insere uma nova linha na tabela com o resultado da batalha
        # Os ? são placeholders — o SQLite substitui pelos valores da tupla
        # Usar ? em vez de f-string previne ataques de SQL Injection
        self.cursor.execute("""
                            INSERT INTO historico (jogador, pokemon_jogador, pokemon_inimigo, resultado)
                            VALUES (?, ?, ?, ?)
                            """, (jogador, pokemon_jogador, pokemon_inimigo, resultado))
        self.conexao.commit()  # Salva imediatamente após cada batalha

    def buscar_historico(self):
        # Busca todos os registros ordenados do mais recente para o mais antigo
        # ORDER BY id DESC: o maior ID é o inserido por último
        self.cursor.execute(
            "SELECT jogador, pokemon_jogador, pokemon_inimigo, resultado FROM historico ORDER BY id DESC")
        return self.cursor.fetchall()  # Retorna uma lista de tuplas com todos os resultados
