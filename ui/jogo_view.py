import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from controllers.jogo_controller import JogoPokemonController


class JogoPokemon(tk.Tk):
    """Interface gráfica principal do jogo de batalhas Pokémon (camada View do MVC).

    Herda de tk.Tk e gerencia a janela principal, telas do jogo (login, seleção,
    batalha, histórico) e efeitos visuais animados.
    """

    # ── Paleta de cores usadas em toda a interface ──
    COR_FUNDO     = "#1a1a2e"  # Fundo principal da janela (azul muito escuro)
    COR_PAINEL    = "#16213e"  # Fundo dos painéis dos Pokémon (azul escuro)
    COR_CABECALHO = "#AFEEEE"  # Cor das barras de título (azul claro)
    HP_VERDE      = "#4dff4d"  # Barra de HP alta (acima de 50%)
    HP_AMARELO    = "#ffff4d"  # Barra de HP média (entre 25% e 50%)
    HP_VERMELHO   = "#ff4d4d"  # Barra de HP baixa (abaixo de 25%)
    FUNDO_HP      = "#555555"  # Cor de fundo da barra de HP (parte vazia)
    COR_TEXTO     = "#2b2b2b"  # Cor escura usada em textos sobre fundo claro
    BOTAO_DESAB   = "#ff6666"  # Cor do botão de ataque sem mana (desabilitado)
    BOTAO_HOVER   = "#66ff66"  # Cor do botão ao passar o mouse por cima

    # Dicionário de cores elementais para os botões de ataque (estética pastel e legível)
    CORES_TIPOS = {
        "Normal": "#C6C6A7",     # Bege/Cinza claro
        "Fogo": "#Ad4a2f",       # Fogo
        "Água": "#87CEFA",       # Azul céu claro
        "Planta": "#7cfc00",     # Verde grama
        "Elétrico": "#fde910",   # Amarelo
        "Sombrio": "#2b3249",    # Marrom claro / Tan
        "Aço": "#B0C4DE"         # Azul metálico claro
    }

    # Cores de hover correspondentes para efeito de foco
    CORES_TIPOS_HOVER = {
        "Normal": "#D8D8BE",
        "Fogo": "#FFB399",
        "Água": "#A0DBFF",
        "Planta": "#B0FFB0",
        "Elétrico": "#FFFFB0",
        "Sombrio": "#E3C8A2",
        "Aço": "#C5D8F0"
    }

    # ── Fontes usadas nos diferentes elementos da tela ──
    FONTE_TITULO  = ("Arial", 24, "bold")   # Título principal da janela
    FONTE_CABEC   = ("Arial", 16, "bold")   # Cabeçalhos das telas
    FONTE_LABEL   = ("Arial", 14)            # Textos e rótulos gerais
    FONTE_BOTAO   = ("Arial", 12, "bold")   # Botões de ação (Entrar, Histórico)
    FONTE_LOG     = ("Arial", 12, "bold")   # Texto do log de batalha
    FONTE_ATAQUE  = ("Arial", 10, "bold")   # Texto nos botões de ataque

    def __init__(self):
        super().__init__()
        self.title("Batalha Pokémon")
        self.geometry("1024x768")
        self.resizable(False, False)
        self.configure(bg=self.COR_FUNDO)

        self.jogo = JogoPokemonController()
        self.botoes_ataque = []
        self.imagens_tipo = {}
        self.imagem_fundo = None

        # Referências salvas para uso nas animações
        self.frame_inimigo = None
        self.frame_jogador = None
        self.lbl_img_inimigo = None
        self.lbl_img_jogador = None

        # Container que envolve todos os widgets
        self.container = tk.Frame(self, bg=self.COR_FUNDO)
        self.container.pack(fill="both", expand=True)

        self._carregar_imagens()
        self._aplicar_fundo()
        self.tela_login()

    # ──────────────────────────────────────────────
    # UTILITÁRIOS GERAIS
    # ──────────────────────────────────────────────

    def limpar_tela(self):
        """Destrói todos os widgets do container, exceto a imagem de fundo."""
        for widget in self.container.winfo_children():
            if widget != getattr(self, 'label_fundo', None):
                widget.destroy()

    def _obter_cor_hp(self, hp_percent):
        """Retorna a cor da barra de HP baseada na porcentagem atual."""
        if hp_percent > 50:
            return self.HP_VERDE
        elif hp_percent > 25:
            return self.HP_AMARELO
        else:
            return self.HP_VERMELHO


    # ──────────────────────────────────────────────
    # CARREGAMENTO DE IMAGENS
    # ──────────────────────────────────────────────

    def _carregar_imagens(self):
        """Carrega e redimensiona os recursos de imagem da pasta assets/."""
        pasta_assets = os.path.join(os.path.dirname(__file__), "..", "assets")

        tipos = {
            "Fogo":     "pokemon_fogo.png",
            "Água":     "pokemon_agua.png",
            "Planta":   "pokemon_planta.png",
            "Elétrico": "pokemon_eletrico.png",
            "Normal":   "pokemon_normal.png",
        }
        TAMANHO_PADRAO = (120, 120)

        for tipo, arquivo in tipos.items():
            caminho = os.path.join(pasta_assets, arquivo)
            if os.path.exists(caminho):
                try:
                    imagem_pil = Image.open(caminho).resize(TAMANHO_PADRAO, Image.Resampling.LANCZOS)
                    self.imagens_tipo[tipo] = ImageTk.PhotoImage(imagem_pil)
                except Exception as e:
                    print(f"Erro ao carregar imagem {tipo}: {e}")
                    self.imagens_tipo[tipo] = None
            else:
                self.imagens_tipo[tipo] = None

        # Carrega a imagem de fundo da arena
        caminho_fundo = os.path.join(pasta_assets, "fundo_jogo.png")
        if os.path.exists(caminho_fundo):
            try:
                imagem_fundo = Image.open(caminho_fundo).resize(
                    (self.winfo_screenwidth(), self.winfo_screenheight()), Image.Resampling.LANCZOS
                )
                self.imagem_fundo = ImageTk.PhotoImage(imagem_fundo)
            except Exception as e:
                print(f"Erro ao carregar fundo: {e}")
                self.imagem_fundo = None

    def _aplicar_fundo(self):
        """Aplica a imagem de fundo no label raiz da janela."""
        if self.imagem_fundo is None:
            return
        self.label_fundo = tk.Label(self.container, image=self.imagem_fundo, bg=self.COR_FUNDO)
        self.label_fundo.image = self.imagem_fundo
        self.label_fundo.place(x=0, y=0, relwidth=1, relheight=1)
        self.label_fundo.lower()

    # ──────────────────────────────────────────────
    # ANIMAÇÕES
    # ──────────────────────────────────────────────

    def _animar_hp_suave(self, pokemon, label, barra, hp_inicial, hp_alvo, passos=20, passo_atual=0):
        """Anima a barra de HP interpolando suavemente os valores."""
        if passo_atual > passos:
            hp_percent = (pokemon.hp_atual / pokemon.hp_maximo) * 100
            label.config(text=f"HP: {pokemon.hp_atual}/{pokemon.hp_maximo}")
            barra.config(bg=self._obter_cor_hp(hp_percent))
            barra.place(relwidth=hp_percent / 100, relheight=1)
            return

        progresso = passo_atual / passos
        progresso_suave = 1 - (1 - progresso) ** 2  # Efeito ease-out
        hp_interpolado = hp_inicial + (hp_alvo - hp_inicial) * progresso_suave
        hp_percent = (hp_interpolado / pokemon.hp_maximo) * 100

        label.config(text=f"HP: {int(hp_interpolado)}/{pokemon.hp_maximo}")
        barra.config(bg=self._obter_cor_hp(hp_percent))
        barra.place(relwidth=max(0, hp_percent / 100), relheight=1)

        self.after(18, lambda: self._animar_hp_suave(
            pokemon, label, barra, hp_inicial, hp_alvo, passos, passo_atual + 1
        ))

    def _flash_tela(self, cor_flash="#ff0000", repeticoes=4, visivel=True):
        """Faz a tela piscar alternando a cor de fundo."""
        if repeticoes <= 0:
            self.configure(bg=self.COR_FUNDO)
            self.container.configure(bg=self.COR_FUNDO)
            return
        cor = cor_flash if visivel else self.COR_FUNDO
        self.configure(bg=cor)
        self.container.configure(bg=cor)
        self.after(80, lambda: self._flash_tela(cor_flash, repeticoes - 1, not visivel))

    def _digitar_texto(self, label_alvo, texto, cor_texto, indice=0):
        """Efeito de máquina de escrever para mensagens de log de batalha."""
        if not label_alvo or not label_alvo.winfo_exists():
            return
        if indice == 0:
            label_alvo.config(text="", fg=cor_texto)
        if indice <= len(texto):
            try:
                label_alvo.config(text=texto[:indice])
            except Exception:
                return
            self.after(22, lambda: self._digitar_texto(label_alvo, texto, cor_texto, indice + 1))

    def _pulsar_log(self, label_alvo, cor_base, cor_pulo, passos=8, subindo=True, passo_atual=0):
        """Faz o fundo de um painel de log pulsar."""
        if not label_alvo or not label_alvo.winfo_exists():
            return
        if passo_atual >= passos:
            try:
                label_alvo.config(bg=self.COR_PAINEL)
            except Exception:
                pass
            return
        progresso = passo_atual / passos
        cor = cor_pulo if (subindo and progresso < 0.5) else cor_base
        try:
            label_alvo.config(bg=cor)
        except Exception:
            return
        self.after(60, lambda: self._pulsar_log(label_alvo, cor_base, cor_pulo, passos, subindo, passo_atual + 1))

    def _animar_vitoria(self):
        """Efeito de piscar verde e pulsar log ao vencer."""
        self._flash_tela(cor_flash=self.HP_VERDE, repeticoes=6)
        self._pulsar_log(self.lbl_log_jogador, self.COR_PAINEL, "#004400", passos=10)

    def _animar_derrota(self):
        """Efeito de piscar vermelho e pulsar log ao perder."""
        self._flash_tela(cor_flash=self.HP_VERMELHO, repeticoes=8)
        self._pulsar_log(self.lbl_log_jogador, self.COR_PAINEL, "#440000", passos=10)

    def _animar_dano_recebido(self, frame_alvo, lbl_img_alvo, cor_flash):
        """Executa a animação completa de dano recebido."""
        self._flash_tela(cor_flash=cor_flash, repeticoes=4)
        self._shake_frame_pack(frame_alvo)
        if lbl_img_alvo and lbl_img_alvo.winfo_exists():
            self._piscar_label(lbl_img_alvo)

    def _shake_frame_pack(self, frame, repeticoes=6, pad=8):
        """Simula um balanço horizontal ajustando a margem (pack)."""
        if frame is None or not frame.winfo_exists():
            return
        if repeticoes <= 0:
            try:
                frame.pack_configure(padx=40)
            except Exception:
                pass
            return
        novo_pad = 40 + pad if repeticoes % 2 == 0 else 40 - pad
        try:
            frame.pack_configure(padx=novo_pad)
        except Exception:
            return
        self.after(45, lambda: self._shake_frame_pack(frame, repeticoes - 1, pad))

    def _piscar_label(self, label, repeticoes=6):
        """Faz o fundo de um label piscar alternando com branco."""
        if label is None or not label.winfo_exists():
            return
        if repeticoes <= 0:
            try:
                label.config(fg=label.cget("fg"))
            except Exception:
                pass
            return
        try:
            cor_atual = label.cget("bg")
            nova_cor = self.COR_PAINEL if cor_atual != "#ffffff" else "#ffffff"
            label.config(bg=nova_cor)
        except Exception:
            return
        self.after(65, lambda: self._piscar_label(label, repeticoes - 1))

    # ──────────────────────────────────────────────
    # TELAS DO JOGO
    # ──────────────────────────────────────────────

    def tela_login(self):
        """Desenha a tela inicial de Login."""
        self.limpar_tela()

        frame_titulo = tk.Frame(self.container, bg=self.COR_CABECALHO, height=80)
        frame_titulo.pack(fill="x")
        tk.Label(frame_titulo, text=" Batalha Pokémon ", font=self.FONTE_TITULO,
                 bg=self.COR_CABECALHO, fg="black").pack(pady=15)

        tk.Label(self.container, text="Bem-vindo ao Torneio!", font=("Arial", 18, "bold"),
                 bg=self.COR_CABECALHO, fg="black").pack(pady=40)
        tk.Label(self.container, text="Digite o nome do Treinador:", font=self.FONTE_LABEL,
                 bg="#9AF26B", fg="black").pack(pady=10)

        self.entry_nome = tk.Entry(self.container, font=self.FONTE_LABEL, width=20,
                                   bg=self.COR_TEXTO, fg="white", insertbackground="white")
        self.entry_nome.pack(pady=10)
        self.entry_nome.focus_set()

        frame_botoes = tk.Frame(self.container, bg=self.COR_FUNDO)
        frame_botoes.pack(pady=30)
        tk.Button(frame_botoes, text="Entrar", font=self.FONTE_BOTAO, bg=self.HP_VERDE,
                  command=self.iniciar_jogo).pack(side="left", padx=10)
        tk.Button(frame_botoes, text="Ver Histórico", font=self.FONTE_BOTAO, bg="#4da6ff",
                  command=self.tela_historico).pack(side="left", padx=10)

    def iniciar_jogo(self):
        """Valida a entrada e inicia a tela de seleção."""
        if not self.jogo.jogador_nome:
            nome_digitado = self.entry_nome.get().strip()
            if not nome_digitado:
                messagebox.showwarning("Aviso", "Por favor, digite seu nome!")
                return
            self.jogo.iniciar_jogo(nome_digitado)
        self.tela_selecao()

    def tela_selecao(self):
        """Desenha a tela de seleção do Pokémon inicial."""
        self.limpar_tela()
        cabecalho = tk.Frame(self.container, bg=self.COR_CABECALHO)
        cabecalho.pack(fill="x")
        tk.Label(cabecalho, text=f"Treinador {self.jogo.jogador_nome}, escolha seu Pokémon!",
                 font=self.FONTE_CABEC, bg=self.COR_CABECALHO, fg="black").pack(pady=15)

        frame_botoes = tk.Frame(self.container, bg=self.COR_FUNDO)
        frame_botoes.pack(pady=30)

        for pokemon in self.jogo.pokemons_iniciais:
            imagem = self.imagens_tipo.get(pokemon.tipo)
            btn = tk.Button(
                frame_botoes,
                text=f"{pokemon.nome}\n({pokemon.tipo})\nHP: {pokemon.hp_maximo}",
                image=imagem, compound="top",
                bg=pokemon.cor_imagem, fg="black",
                font=("Arial", 11, "bold"), relief="raised", bd=3,
                command=lambda p=pokemon: self.selecionar_pokemon(p)
            )
            btn.pack(side="left", padx=10, pady=10)
            btn.bind("<Enter>", lambda e, b=btn: b.config(relief="sunken", bd=4))
            btn.bind("<Leave>", lambda e, b=btn: b.config(relief="raised", bd=3))

    def selecionar_pokemon(self, escolhido):
        """Salva a seleção e avança na sequência de lutas."""
        self.jogo.selecionar_pokemon(escolhido)
        self.preparar_proxima_batalha()

    def preparar_proxima_batalha(self):
        """Prepara o próximo duelo do torneio."""
        if not self.jogo.preparar_proxima_batalha():
            messagebox.showinfo("Vitória Final!", "Você derrotou todos e zerou o jogo!")
            self.jogo.jogador_nome = ""
            self.tela_login()
            return
        self.tela_batalha()

    def tela_batalha(self):
        """Monta a arena de batalha (painéis e botões)."""
        self.limpar_tela()
        self.frame_inimigo = None
        self.frame_jogador = None
        self.lbl_img_inimigo = None
        self.lbl_img_jogador = None
        self.lbl_log_inimigo = None
        self.lbl_log_jogador = None

        cabecalho = tk.Frame(self.container, bg=self.COR_CABECALHO)
        cabecalho.pack(fill="x")

        self._criar_painel_pokemon(self.jogo.oponente_atual, "e", eh_inimigo=True)
        self._criar_painel_pokemon(self.jogo.pokemon_jogador, "w", eh_inimigo=False)

        self._digitar_texto(self.lbl_log_jogador, "A batalha começou! Seu turno.", "#00ffcc")

        self.frame_ataques = tk.Frame(self.container, bg=self.COR_FUNDO)
        self.frame_ataques.pack(pady=10)
        self.criar_botoes_ataque()

    def _criar_painel_pokemon(self, pokemon, anchor, eh_inimigo):
        """Cria o painel individual contendo HP, imagem e log de um Pokémon."""
        frame = tk.Frame(self.container, bg=self.COR_PAINEL, relief="raised", bd=3)
        frame.pack(fill="x", pady=15, padx=40)

        tk.Label(frame, text=f"{pokemon.nome} ({pokemon.tipo})", font=("Arial", 15, "bold"),
                 bg=self.COR_PAINEL, fg=pokemon.cor_imagem).pack(anchor=anchor, pady=10)

        imagem = self.imagens_tipo.get(pokemon.tipo)
        lbl_img = None
        if imagem:
            lbl_img = tk.Label(frame, image=imagem, bg=self.COR_PAINEL)
            lbl_img.pack(anchor=anchor, pady=5)
            frame.imagem = imagem
        else:
            lbl_img = tk.Label(frame, bg=pokemon.cor_imagem, width=14, height=5)
            lbl_img.pack(anchor=anchor, pady=5)

        frame_hp = tk.Frame(frame, bg=self.COR_TEXTO, height=25)
        frame_hp.pack(anchor=anchor, fill="x", padx=20, pady=10)

        hp_percent = (pokemon.hp_atual / pokemon.hp_maximo) * 100
        cor_hp = self._obter_cor_hp(hp_percent)

        tk.Label(frame_hp, bg=self.FUNDO_HP, height=1).pack(fill="x")
        barra = tk.Label(frame_hp, bg=cor_hp, height=1)
        barra.place(relwidth=hp_percent / 100, relheight=1)

        label_hp = tk.Label(frame_hp, text=f"HP: {pokemon.hp_atual}/{pokemon.hp_maximo}",
                             font=("Arial", 10, "bold"), bg=self.COR_TEXTO, fg="white")
        label_hp.pack(fill="x", expand=True)

        lbl_log_local = tk.Label(frame, text="", font=self.FONTE_LOG, bg=self.COR_PAINEL, fg="#00ffcc", height=2)
        lbl_log_local.pack(pady=5, fill="x", padx=20)

        if eh_inimigo:
            self.lbl_hp_inimigo    = label_hp
            self.barra_hp_inimigo  = barra
            self.frame_inimigo     = frame
            self.lbl_img_inimigo   = lbl_img
            self.lbl_log_inimigo   = lbl_log_local
        else:
            self.lbl_hp_jogador    = label_hp
            self.barra_hp_jogador  = barra
            self.frame_jogador     = frame
            self.lbl_img_jogador   = lbl_img
            self.lbl_log_jogador   = lbl_log_local

    def criar_botoes_ataque(self):
        """Cria e atualiza os botões de ação de ataque com base na mana."""
        for widget in self.frame_ataques.winfo_children():
            widget.destroy()
        self.botoes_ataque = []

        for indice, ataque in enumerate(self.jogo.pokemon_jogador.ataques):
            tem_mana = ataque.tem_mana()
            texto = (
                f"{ataque.nome}\n"
                f"Dano: {ataque.dano} | Acerto: {int(ataque.precisao * 100)}%\n"
                f"Mana: {ataque.mana_atual}/{ataque.mana_maxima}"
            )
            cor_base = self.CORES_TIPOS.get(ataque.tipo, "#C6C6A7")
            cor_hover = self.CORES_TIPOS_HOVER.get(ataque.tipo, "#D8D8BE")

            btn = tk.Button(
                self.frame_ataques, text=texto, font=self.FONTE_ATAQUE,
                bg=cor_base if tem_mana else self.BOTAO_DESAB,
                fg="black" if tem_mana else "white",
                width=24, height=3,
                relief="raised" if tem_mana else "sunken", bd=2,
                state="normal" if tem_mana else "disabled",
                command=lambda a=ataque: self.turno_jogador(a)
            )
            btn.grid(row=0, column=indice, padx=10, pady=5, sticky="ew")
            self.botoes_ataque.append(btn)
            if tem_mana:
                btn.bind("<Enter>", lambda e, b=btn, c_h=cor_hover: b.config(bg=c_h, relief="sunken"))
                btn.bind("<Leave>", lambda e, b=btn, c_b=cor_base: b.config(bg=c_b, relief="raised"))

    def _atualizar_hp_barra(self, pokemon, label, barra, hp_antes):
        """Inicia a animação gradual do HP."""
        self._animar_hp_suave(pokemon, label, barra, hp_antes, pokemon.hp_atual)

    def atualizar_interface(self, hp_inimigo_antes=None, hp_jogador_antes=None):
        """Mantém barras de HP e painéis atualizados."""
        if hp_inimigo_antes is not None:
            self._atualizar_hp_barra(
                self.jogo.oponente_atual, self.lbl_hp_inimigo,
                self.barra_hp_inimigo, hp_inimigo_antes
            )
        if hp_jogador_antes is not None:
            self._atualizar_hp_barra(
                self.jogo.pokemon_jogador, self.lbl_hp_jogador,
                self.barra_hp_jogador, hp_jogador_antes
            )
        self.criar_botoes_ataque()

    # ──────────────────────────────────────────────
    # LÓGICA DE TURNO
    # ──────────────────────────────────────────────

    def turno_jogador(self, ataque_escolhido):
        """Processa a jogada iniciada pelo clique de ataque do jogador."""
        if not ataque_escolhido.tem_mana():
            return

        for btn in self.botoes_ataque:
            btn.config(state="disabled")

        self.lbl_log_inimigo.config(text="")

        hp_inimigo_antes = self.jogo.oponente_atual.hp_atual
        dano = self.jogo.atacar_oponente(ataque_escolhido)

        if dano:
            self._animar_dano_recebido(self.frame_inimigo, self.lbl_img_inimigo, "#ff6600")
            msg = f"✅ {self.jogo.pokemon_jogador.nome} usou {ataque_escolhido.nome} e causou {dano} de dano!"
            self._digitar_texto(self.lbl_log_jogador, msg, self.HP_VERDE)
        else:
            self._flash_tela(cor_flash="#003366", repeticoes=3)
            msg = f"❌ {self.jogo.pokemon_jogador.nome} tentou {ataque_escolhido.nome}, mas falhou!"
            self._digitar_texto(self.lbl_log_jogador, msg, self.HP_VERMELHO)

        self.atualizar_interface(hp_inimigo_antes=hp_inimigo_antes)

        if not self.jogo.oponente_atual.esta_vivo():
            self.after(1600, self.finalizar_batalha, "Vitória")
            return

        self.after(1600, self.turno_adversario)

    def turno_adversario(self):
        """Processa a rodada da inteligência artificial inimiga."""
        self.lbl_log_jogador.config(text="")

        hp_jogador_antes = self.jogo.pokemon_jogador.hp_atual
        ataque_inimigo, dano = self.jogo.atacar_jogador()

        if ataque_inimigo is None:
            msg = f"{self.jogo.oponente_atual.nome} está sem mana e passou o turno!"
            self._digitar_texto(self.lbl_log_inimigo, msg, "#00ffcc")
        else:
            if dano:
                self._animar_dano_recebido(self.frame_jogador, self.lbl_img_jogador, "#ff0000")
                msg = f"⚠️ {self.jogo.oponente_atual.nome} usou {ataque_inimigo.nome} e causou {dano} de dano!"
                self._digitar_texto(self.lbl_log_inimigo, msg, self.HP_AMARELO)
            else:
                self._flash_tela(cor_flash="#003366", repeticoes=3)
                msg = f"💨 {self.jogo.oponente_atual.nome} tentou {ataque_inimigo.nome} e ERROU!"
                self._digitar_texto(self.lbl_log_inimigo, msg, "#4da6ff")

            self.atualizar_interface(hp_jogador_antes=hp_jogador_antes)

        if not self.jogo.pokemon_jogador.esta_vivo():
            self.after(1600, self.finalizar_batalha, "Derrota")
            return

        delay_reabilitar = len(msg) * 22 + 300
        self.after(delay_reabilitar, self._reabilitar_botoes)

    def _reabilitar_botoes(self):
        """Reabilita os botões de ação se os widgets ainda existirem."""
        for btn in self.botoes_ataque:
            if btn.winfo_exists():
                btn.config(state="normal")

    def finalizar_batalha(self, resultado):
        """Encerra o combate salvando o log e decidindo a próxima tela."""
        self.jogo.registrar_batalha(resultado)

        if resultado == "Vitória":
            self._animar_vitoria()
            self.after(500, lambda: messagebox.showinfo(
                "Vitória!", f"Você derrotou o {self.jogo.oponente_atual.nome}!"
            ))
            self.after(600, self.preparar_proxima_batalha)
        else:
            self._animar_derrota()
            self.after(500, lambda: messagebox.showerror(
                "Derrota", f"Seu {self.jogo.pokemon_jogador.nome} desmaiou... Fim de jogo."
            ))
            self.jogo.jogador_nome = ""
            self.after(600, self.tela_login)

    # ──────────────────────────────────────────────
    # HISTÓRICO DE BATALHAS
    # ──────────────────────────────────────────────

    def tela_historico(self):
        """Exibe uma janela secundária com a listagem do histórico."""
        registros = self.jogo.buscar_historico()
        janela_hist = tk.Toplevel(self)
        janela_hist.title("Histórico de Batalhas")
        janela_hist.geometry("600x450")
        janela_hist.configure(bg=self.COR_FUNDO)

        cabecalho = tk.Frame(janela_hist, bg=self.COR_CABECALHO)
        cabecalho.pack(fill="x")
        tk.Label(cabecalho, text="Histórico de Batalhas Registradas", font=self.FONTE_CABEC,
                 bg=self.COR_CABECALHO, fg="black").pack(pady=10)

        frame_lista = tk.Frame(janela_hist, bg=self.COR_FUNDO)
        frame_lista.pack(fill="both", expand=True, padx=20, pady=10)

        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side="right", fill="y")

        lista = tk.Listbox(frame_lista, yscrollcommand=scrollbar.set, font=self.FONTE_LABEL,
                           bg=self.COR_PAINEL, fg="white")
        for jogador, pokemon_jogador, pokemon_inimigo, resultado in registros:
            lista.insert("end", f"Treinador: {jogador} | {pokemon_jogador} vs {pokemon_inimigo} -> {resultado}")

        lista.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=lista.yview)
