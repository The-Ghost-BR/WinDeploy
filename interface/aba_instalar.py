"""
interface/aba_instalar.py
==========================
Conteúdo da aba "Instalar Programas": mostra os checkboxes com base no
catálogo de dados/programas.py, com dica ao passar o mouse e um indicador
visual de status (instalando / instalado / erro) ao lado de cada item.

Antes de instalar qualquer coisa, verifica se o winget existe no PC e
tenta atualizá-lo, pra evitar erros por versão desatualizada.
"""

import threading
from tkinter import messagebox

import customtkinter as ctk

from core.instalador import atualizar_winget, instalar_programa, verificar_winget
from dados.programas import PROGRAMAS
from interface.tooltip import ToolTip

ACCENT = "#7C6FF0"
ACCENT_HOVER = "#6C5FE0"
TEXT_MUTED = "#9A9AA5"
VERDE = "#4ADE80"
VERMELHO = "#F87171"


def montar_aba_instalar(aba, janela):
    """
    aba    -> o frame da aba onde vamos desenhar os checkboxes e o botão
    janela -> a JanelaPrincipal, usada pra escrever no log e mexer na barra
    """
    checkboxes = {}
    status_labels = {}

    scroll = ctk.CTkScrollableFrame(aba, fg_color="transparent")
    scroll.pack(fill="both", expand=True, padx=4, pady=4)

    for categoria, apps in PROGRAMAS.items():
        ctk.CTkLabel(
            scroll, text=categoria, text_color=ACCENT,
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", pady=(12, 6))

        for nome, info in apps.items():
            linha = ctk.CTkFrame(scroll, fg_color="transparent")
            linha.pack(fill="x", pady=4, padx=6)

            cb = ctk.CTkCheckBox(linha, text=nome, fg_color=ACCENT, hover_color=ACCENT_HOVER)
            cb.pack(side="left")
            ToolTip(cb, info["descricao"])

            status = ctk.CTkLabel(linha, text="", text_color=TEXT_MUTED, font=ctk.CTkFont(size=12))
            status.pack(side="left", padx=(10, 0))

            checkboxes[nome] = (cb, info["id"])
            status_labels[nome] = status

    def ao_clicar_instalar():
        selecionados = [(nome, wid) for nome, (cb, wid) in checkboxes.items() if cb.get()]
        if not selecionados:
            janela.log("Nenhum programa selecionado.")
            return

        if not verificar_winget():
            messagebox.showerror(
                "winget não encontrado",
                "O winget não foi encontrado neste computador.\n\n"
                "Instale o 'App Installer' pela Microsoft Store e tente novamente."
            )
            janela.log("ERRO: winget não encontrado neste PC.")
            return

        threading.Thread(target=instalar_em_segundo_plano, args=(selecionados,), daemon=True).start()

    def instalar_em_segundo_plano(selecionados):
        atualizar_winget(janela.log)

        total = len(selecionados)
        for i, (nome, wid) in enumerate(selecionados, start=1):
            status_labels[nome].configure(text="⏳ instalando...", text_color=ACCENT)
            janela.progresso((i - 0.5) / total)

            sucesso = instalar_programa(nome, wid, janela.log)

            if sucesso:
                status_labels[nome].configure(text="✅ instalado", text_color=VERDE)
            else:
                status_labels[nome].configure(text="❌ erro", text_color=VERMELHO)

            janela.progresso(i / total)

        janela.log("Instalação de programas concluída!")
        janela.progresso(0)

    ctk.CTkButton(
        aba, text="Instalar selecionados", height=38, corner_radius=10,
        fg_color=ACCENT, hover_color=ACCENT_HOVER,
        command=ao_clicar_instalar
    ).pack(pady=(12, 4))