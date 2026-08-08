"""
main.py
=======
Ponto de entrada do app. Verifica permissão de administrador, abre a
janela e tenta aplicar o efeito Mica/Acrylic.
Toda a lógica de verdade mora dentro de core/, dados/ e interface/.
"""

import os

import customtkinter as ctk

from core.sistema import aplicar_efeito_janela, is_admin, relaunch_as_admin
from interface.janela_principal import JanelaPrincipal

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


if __name__ == "__main__":
    if os.name == "nt" and not is_admin():
        relaunch_as_admin()

    app = JanelaPrincipal()

    # Espera a janela existir de verdade na tela antes de tentar aplicar o efeito
    app.after(10, lambda: aplicar_efeito_janela(app))

    app.mainloop()