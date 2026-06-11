import random

from data.database import BancoDeDados
from models.ataque import Ataque
from models.pokemon import (
    PokemonAgua,
    PokemonEletrico,
    PokemonFogo,
    PokemonNormal,
    PokemonPlanta,
)


class JogoPokemonController:
    """Controlador da lógica do jogo (camada Controller do padrão MVC).

    Centraliza todas as regras: criação dos Pokémon, turnos, lógica de combate e
    persistência no banco de dados. A interface gráfica (View) consome este controlador.
    """

    def __init__(self):
        self.banco = BancoDeDados()
        self.jogador_nome = ""
        self.pokemon_jogador = None
        self.oponentes = []
        self.oponente_atual = None
        self.pokemons_iniciais = self._criar_pokemons_iniciais()

    def iniciar_jogo(self, nome):
        """Inicializa o jogo definindo o nome do jogador e recriando os Pokémon."""
        self.jogador_nome = nome.strip()
        self.pokemons_iniciais = self._criar_pokemons_iniciais()

    def _criar_pokemons_iniciais(self):
        """Cria e retorna a lista com os 5 Pokémon disponíveis para seleção."""
        return [
            PokemonFogo(
                "Charmander",
                120,
                [
                    Ataque("Arranhão", 15, 15, 1.0, "Normal"),
                    Ataque("Brasa", 22, 10, 0.85, "Fogo"),
                    Ataque("Fúria", 26, 8, 0.75, "Normal"),
                    Ataque("Lança-Chamas", 45, 3, 0.45, "Fogo"),
                ],
                "#ff4d4d",
                "Fogo",
            ),
            PokemonAgua(
                "Squirtle",
                135,
                [
                    Ataque("Investida", 14, 15, 1.0, "Normal"),
                    Ataque("Pistola d'Água", 20, 10, 0.90, "Água"),
                    Ataque("Mordida", 25, 8, 0.80, "Sombrio"),
                    Ataque("Hidrobomba", 42, 3, 0.50, "Água"),
                ],
                "#4da6ff",
                "Água",
            ),
            PokemonPlanta(
                "Bulbasaur",
                125,
                [
                    Ataque("Pancada", 15, 15, 1.0, "Normal"),
                    Ataque("Chicote de Vinha", 21, 10, 0.85, "Planta"),
                    Ataque("Folha Navalha", 27, 8, 0.75, "Planta"),
                    Ataque("Raio Solar", 48, 2, 0.40, "Planta"),
                ],
                "#4dff4d",
                "Planta",
            ),
            PokemonEletrico(
                "Pikachu",
                110,
                [
                    Ataque("Ataque Rápido", 16, 15, 1.0, "Normal"),
                    Ataque("Choque do Trovão", 24, 10, 0.85, "Elétrico"),
                    Ataque("Cauda de Ferro", 28, 8, 0.70, "Aço"),
                    Ataque("Trovão", 50, 3, 0.40, "Elétrico"),
                ],
                "#ffff4d",
                "Elétrico",
            ),
            PokemonNormal(
                "Eevee",
                130,
                [
                    Ataque("Investida", 15, 15, 1.0, "Normal"),
                    Ataque("Ataque Rápido", 18, 10, 0.95, "Normal"),
                    Ataque("Mordida", 26, 8, 0.80, "Sombrio"),
                    Ataque("Último Recurso", 40, 3, 0.55, "Normal"),
                ],
                "#d2a679",
                "Normal",
            ),
        ]

    def selecionar_pokemon(self, pokemon):
        """Define o Pokémon do jogador e embaralha a lista de oponentes."""
        self.pokemon_jogador = pokemon
        self.oponentes = [pok for pok in self.pokemons_iniciais if pok != pokemon]
        random.shuffle(self.oponentes)

    def preparar_proxima_batalha(self):
        """Prepara o próximo oponente na fila. Retorna False se não houver mais oponentes."""
        if not self.oponentes:
            return False

        self.oponente_atual = self.oponentes.pop(0)
        self.pokemon_jogador.preparar_para_nova_batalha()
        self.oponente_atual.preparar_para_nova_batalha()
        return True

    def atacar_oponente(self, ataque):
        """Executa um ataque contra o oponente atual.

        Consome mana do ataque selecionado e calcula o dano causado.
        """
        if not ataque.tem_mana():
            return 0

        ataque.usar_mana()
        return self.pokemon_jogador.atacar(self.oponente_atual, ataque)

    def atacar_jogador(self):
        """Turno do oponente controlado por IA.

        Seleciona aleatoriamente um ataque disponível que possua mana.
        """
        ataques_disponiveis = [atk for atk in self.oponente_atual.ataques if atk.tem_mana()]
        if not ataques_disponiveis:
            return None, None

        ataque_inimigo = random.choice(ataques_disponiveis)
        ataque_inimigo.usar_mana()
        dano = self.oponente_atual.atacar(self.pokemon_jogador, ataque_inimigo)
        return ataque_inimigo, dano

    def registrar_batalha(self, resultado):
        """Persiste o resultado da batalha no histórico do banco de dados SQLite."""
        self.banco.registrar_batalha(
            self.jogador_nome,
            self.pokemon_jogador.nome,
            self.oponente_atual.nome,
            resultado,
        )

    def buscar_historico(self):
        """Recupera o histórico de batalhas registrado."""
        return self.banco.buscar_historico()
