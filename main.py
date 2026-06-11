# Importa a classe principal da interface gráfica (View)
from ui.jogo_view import JogoPokemon


# Bloco que garante que este arquivo só rode quando executado diretamente
if __name__ == "__main__":
    app = JogoPokemon()  # Cria a janela principal do jogo
    app.mainloop()       # Inicia o loop de eventos do Tkinter
