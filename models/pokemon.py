import random
from .ataque import Ataque  


# ──────────────────────────────────────────────
# TABELA DE EFETIVIDADE DE TIPOS (CARTA DE TIPOS)
# [tipo_ataque][tipo_defensor] -> multiplicador
# ──────────────────────────────────────────────
TABELA_EFETIVIDADE = {
    "Normal": {},
    "Fogo": {
        "Planta": 2.0,
        "Água": 0.5,
        "Fogo": 0.5,
    },
    "Água": {
        "Fogo": 2.0,
        "Planta": 0.5,
        "Água": 0.5,
    },
    "Planta": {
        "Água": 2.0,
        "Fogo": 0.5,
        "Planta": 0.5,
    },
    "Elétrico": {
        "Água": 2.0,
        "Planta": 0.5,
        "Elétrico": 0.5,
    },
    "Sombrio": {},
    "Aço": {
        "Fogo": 0.5,
        "Água": 0.5,
        "Elétrico": 0.5,
    }
}


def obter_multiplicador_dano(tipo_ataque, tipo_defensor):
    """Retorna o multiplicador de dano com base no tipo do ataque e no tipo do defensor."""
    return TABELA_EFETIVIDADE.get(tipo_ataque, {}).get(tipo_defensor, 1.0)


# ──────────────────────────────────────────────
# SUPERCLASSE BASE — todos os tipos herdam daqui
# ──────────────────────────────────────────────
class Pokemon:
    """Superclasse Base"""

    def __init__(self, nome, hp, lista_ataques, cor_imagem, tipo):
        self.nome = nome              # Nome do Pokémon (ex: "Charmander")
        self.hp_maximo = hp          # HP máximo — nunca muda durante a batalha
        self.hp_atual = hp           # HP atual — vai diminuindo conforme recebe dano
        self.ataques = lista_ataques # Lista de objetos Ataque que o Pokémon pode usar
        self.cor_imagem = cor_imagem # Cor hexadecimal usada na interface (ex: "#ff4d4d")
        self.tipo = tipo             # Tipo do Pokémon: "Fogo", "Água", "Planta", etc.

    def receber_dano(self, quantidade):
        # Subtrai o dano recebido do HP atual
        self.hp_atual -= quantidade
        # Garante que o HP nunca fique negativo
        if self.hp_atual < 0:
            self.hp_atual = 0

    def calcular_multiplicador(self, tipo_ataque, tipo_oponente):
        # Retorna o multiplicador de dano com base no tipo do ataque e do oponente
        return obter_multiplicador_dano(tipo_ataque, tipo_oponente)

    def atacar(self, oponente, ataque):
        # Sorteia um número entre 0.0 e 1.0 para verificar se o ataque acerta
        chance_sorteada = random.random()
        if chance_sorteada <= ataque.precisao:
            # Ataque acertou: aplica o multiplicador do tipo do ataque contra o tipo do oponente
            multiplicador = self.calcular_multiplicador(ataque.tipo, oponente.tipo)
            dano_final = int(ataque.dano * multiplicador)  # int() arredonda para baixo
            oponente.receber_dano(dano_final)
            return dano_final  # Retorna o dano causado
        return 0  # Ataque errou: retorna 0

    def esta_vivo(self):
        # Retorna True enquanto o Pokémon tiver HP restante
        return self.hp_atual > 0

    def preparar_para_nova_batalha(self):
        # Restaura o HP ao máximo e recarrega a mana de todos os ataques
        # Chamado antes de cada batalha para resetar o estado do Pokémon
        self.hp_atual = self.hp_maximo
        for atk in self.ataques:
            atk.restaurar_mana()


# ──────────────────────────────────────────────
# SUBCLASSES POR TIPO (Herança)
# ──────────────────────────────────────────────

# Fogo: herda da superclasse Pokemon
class PokemonFogo(Pokemon):
    pass


# Água: herda da superclasse Pokemon
class PokemonAgua(Pokemon):
    pass


# Planta: herda da superclasse Pokemon
class PokemonPlanta(Pokemon):
    pass


# Elétrico: herda da superclasse Pokemon
class PokemonEletrico(Pokemon):
    pass


# Normal: herda da superclasse Pokemon
class PokemonNormal(Pokemon):
    pass
