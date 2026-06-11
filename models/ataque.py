# Representa um ataque que um Pokémon pode usar durante a batalha
class Ataque:

    def __init__(self, nome, dano, mana_maxima, precisao, tipo="Normal"):
        self.nome = nome                  # Nome do ataque (ex: "Lança-Chamas")
        self.dano = dano                  # Quantidade de dano que o ataque causa
        self.mana_maxima = mana_maxima    # Total de usos disponíveis do ataque
        self.mana_atual = mana_maxima     # Usos restantes (começa cheio)
        self.precisao = precisao          # Chance de acertar: valor entre 0.0 e 1.0 (ex: 0.85 = 85%)
        self.tipo = tipo                  # Tipo elemental do ataque (ex: "Fogo", "Normal")

    def tem_mana(self):
        # Retorna True se ainda há usos disponíveis para este ataque
        return self.mana_atual > 0

    def usar_mana(self):
        # Consome 1 uso do ataque. Retorna True se conseguiu, False se já estava vazio
        if self.tem_mana():
            self.mana_atual -= 1
            return True
        return False

    def restaurar_mana(self):
        # Recarrega os usos para o valor máximo
        self.mana_atual = self.mana_maxima
