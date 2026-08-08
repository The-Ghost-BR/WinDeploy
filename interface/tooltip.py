"""
interface/tooltip.py
=====================
Componente reutilizável: um pequeno balão de texto que aparece quando o
mouse fica parado em cima de um widget (checkbox, botão, etc).

Uso em qualquer aba:
    ToolTip(algum_widget, "Texto explicando o que isso faz")
"""

import customtkinter as ctk


class ToolTip:
    def __init__(self, widget, texto: str, atraso_ms: int = 450):
        self.widget = widget
        self.texto = texto
        self.atraso_ms = atraso_ms
        self.janela_popup = None
        self.id_agendamento = None

        widget.bind("<Enter>", self._ao_entrar, add="+")
        widget.bind("<Leave>", self._ao_sair, add="+")

    def _ao_entrar(self, event=None):
        self.id_agendamento = self.widget.after(self.atraso_ms, self._mostrar)

    def _ao_sair(self, event=None):
        if self.id_agendamento:
            self.widget.after_cancel(self.id_agendamento)
            self.id_agendamento = None
        self._esconder()

    def _mostrar(self):
        if self.janela_popup is not None:
            return

        x = self.widget.winfo_rootx() + 16
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 8

        self.janela_popup = ctk.CTkToplevel(self.widget)
        self.janela_popup.wm_overrideredirect(True)
        self.janela_popup.wm_geometry(f"+{x}+{y}")
        self.janela_popup.attributes("-topmost", True)

        ctk.CTkLabel(
            self.janela_popup,
            text=self.texto,
            fg_color="#1F1F27",
            text_color="#F4F4F5",
            corner_radius=8,
            font=ctk.CTkFont(size=11),
            wraplength=260,
            justify="left",
        ).pack(ipadx=10, ipady=6)

    def _esconder(self):
        if self.janela_popup is not None:
            self.janela_popup.destroy()
            self.janela_popup = None