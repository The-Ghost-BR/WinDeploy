"""
interface/janela_principal.py
==============================
A janela do app: título, abas, área de log e barra de progresso.
"""

import queue

import customtkinter as ctk

from core.sistema import caminho_recurso
from interface.aba_instalar import montar_aba_instalar
from interface.aba_otimizacao import montar_aba_otimizacao

# Cores usadas no app inteiro - pra mudar o visual no futuro, mexe só aqui.
ACCENT = "#7C6FF0"
ACCENT_HOVER = "#6C5FE0"
CARD = "#18181E"
BG = "#0E0E12"
BORDER = "#27272F"
TEXT_MUTED = "#9A9AA5"

LARGURA_JANELA = 680
ALTURA_JANELA = 800


class JanelaPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("WinDeploy")
        self.configure(fg_color=BG)
        self.resizable(False, False)

        self._definir_icone()
        self._centralizar_janela()

        # Filas usadas pelas abas para falar com a tela sem travar
        # (tarefas em segundo plano não podem mexer direto nos widgets)
        self.fila_log = queue.Queue()
        self.fila_progresso = queue.Queue()

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=28, pady=24)

        self._montar_header()
        self._montar_abas()
        self._montar_rodape()

        self.after(200, self._processar_fila)

    def _definir_icone(self):
        """Define o ícone da janela e da barra de tarefas (separado do ícone do .exe)."""
        try:
            self.iconbitmap(caminho_recurso("assets/WinDeploy.ico"))
        except Exception:
            pass  # se não achar o ícone, só segue sem ele - não trava o app

    def _centralizar_janela(self):
        """Calcula o centro da tela do usuário e posiciona a janela lá."""
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()

        x = (largura_tela - LARGURA_JANELA) // 2
        y = (altura_tela - ALTURA_JANELA) // 2

        self.geometry(f"{LARGURA_JANELA}x{ALTURA_JANELA}+{x}+{y}")

    def _montar_header(self):
        header = ctk.CTkFrame(self.container, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            header, text="WinDeploy",
            font=ctk.CTkFont(size=26, weight="bold"),
            justify="center"
        ).pack(anchor="center")

        ctk.CTkLabel(
            header,
            text="Instale programas e otimize o Windows em poucos cliques.",
            text_color=TEXT_MUTED,
            font=ctk.CTkFont(size=13),
            justify="center"
        ).pack(anchor="center", pady=(4, 0))

    def _montar_abas(self):
        self.tabview = ctk.CTkTabview(
            self.container,
            fg_color=CARD,
            border_color=BORDER,
            border_width=1,
            corner_radius=14,
            segmented_button_selected_color=ACCENT,
            segmented_button_selected_hover_color=ACCENT_HOVER,
        )
        self.tabview.pack(fill="both", expand=True, pady=(0, 16))

        self.aba_instalar = self.tabview.add("Instalar Programas")
        self.aba_otimizacao = self.tabview.add("Otimização")

        montar_aba_instalar(self.aba_instalar, self)
        montar_aba_otimizacao(self.aba_otimizacao, self)

    def _montar_rodape(self):
        self.log_box = ctk.CTkTextbox(
            self.container,
            height=110,
            corner_radius=10,
            fg_color="#0A0A0D",
            text_color="#4ADE80",
            font=ctk.CTkFont(family="Consolas", size=11),
        )
        self.log_box.pack(fill="x", pady=(0, 12))
        self.log_box.configure(state="disabled")

        self.barra = ctk.CTkProgressBar(self.container, height=10, corner_radius=10, progress_color=ACCENT)
        self.barra.set(0)
        self.barra.pack(fill="x")

    def log(self, texto: str):
        """Qualquer parte do app pode chamar janela.log('mensagem') pra escrever no console visual."""
        self.fila_log.put(texto)

    def progresso(self, valor: float):
        """
        Qualquer parte do app pode chamar janela.progresso(0.5) pra mover a barra
        pra 50%. Não mexe na barra direto - só avisa a fila, com segurança.
        """
        self.fila_progresso.put(valor)

    def _processar_fila(self):
        # Log: escreve todas as mensagens que chegaram
        try:
            while True:
                texto = self.fila_log.get_nowait()
                self.log_box.configure(state="normal")
                self.log_box.insert("end", texto + "\n")
                self.log_box.see("end")
                self.log_box.configure(state="disabled")
        except queue.Empty:
            pass

        # Progresso: pega só o último valor que chegou (evita a barra "engasgar")
        ultimo_valor = None
        try:
            while True:
                ultimo_valor = self.fila_progresso.get_nowait()
        except queue.Empty:
            pass
        if ultimo_valor is not None:
            self.barra.set(ultimo_valor)

        self.after(200, self._processar_fila)