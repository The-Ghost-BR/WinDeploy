"""
interface/aba_otimizacao.py
============================
Conteúdo da aba "Otimização": ajustes gerais (telemetria, energia, limpeza,
TDR), remoção seletiva de bloatware, e itens de inicialização detectados
no PC do usuário. Cada item tem dica ao passar o mouse e indicador visual
de status ao aplicar.
"""

import threading

import customtkinter as ctk

from core.otimizador import (
    ativar_alto_desempenho,
    aplicar_tdr_delay,
    desativar_item_inicializacao,
    desativar_telemetria,
    limpar_temporarios,
    listar_itens_inicializacao,
    remover_bloatware,
)
from dados.bloatware import BLOATWARE
from interface.tooltip import ToolTip

ACCENT = "#7C6FF0"
ACCENT_HOVER = "#6C5FE0"
TEXT_MUTED = "#9A9AA5"
VERDE = "#4ADE80"
VERMELHO = "#F87171"

DESCRICAO_TELEMETRIA = "Impede o Windows de enviar dados de uso e diagnóstico para a Microsoft."
DESCRICAO_ENERGIA = "Troca o plano de energia para priorizar desempenho em vez de economia."
DESCRICAO_LIMPEZA = "Apaga arquivos temporários acumulados nas pastas do usuário e do Windows."
DESCRICAO_TDR = "Aumenta o tempo que o Windows espera antes de reiniciar o driver de vídeo, evitando crashes em jogos ou tarefas pesadas."
DESCRICAO_STARTUP = "Programa configurado para abrir automaticamente sempre que o Windows liga."


def montar_aba_otimizacao(aba, janela):
    """
    aba    -> o frame da aba onde vamos desenhar tudo
    janela -> a JanelaPrincipal, usada pra escrever no log e mexer na barra
    """
    checkboxes_bloatware = {}
    status_bloatware = {}
    checkboxes_startup = {}
    status_startup = {}

    var_telemetria = ctk.BooleanVar(value=False)
    var_energia = ctk.BooleanVar(value=False)
    var_limpeza = ctk.BooleanVar(value=False)
    var_tdr = ctk.BooleanVar(value=False)

    scroll = ctk.CTkScrollableFrame(aba, fg_color="transparent")
    scroll.pack(fill="both", expand=True, padx=4, pady=4)

    # ---------- Ajustes gerais ----------
    ctk.CTkLabel(
        scroll, text="Ajustes gerais", text_color=ACCENT,
        font=ctk.CTkFont(size=13, weight="bold")
    ).pack(anchor="w", pady=(6, 6))

    cb_telemetria = ctk.CTkCheckBox(
        scroll, text="Desativar telemetria da Microsoft", variable=var_telemetria,
        fg_color=ACCENT, hover_color=ACCENT_HOVER
    )
    cb_telemetria.pack(anchor="w", pady=4, padx=6)
    ToolTip(cb_telemetria, DESCRICAO_TELEMETRIA)

    cb_energia = ctk.CTkCheckBox(
        scroll, text="Ativar plano de energia de alto desempenho", variable=var_energia,
        fg_color=ACCENT, hover_color=ACCENT_HOVER
    )
    cb_energia.pack(anchor="w", pady=4, padx=6)
    ToolTip(cb_energia, DESCRICAO_ENERGIA)

    cb_limpeza = ctk.CTkCheckBox(
        scroll, text="Limpar arquivos temporários", variable=var_limpeza,
        fg_color=ACCENT, hover_color=ACCENT_HOVER
    )
    cb_limpeza.pack(anchor="w", pady=4, padx=6)
    ToolTip(cb_limpeza, DESCRICAO_LIMPEZA)

    cb_tdr = ctk.CTkCheckBox(
        scroll, text="Ajustar TDR do driver de vídeo", variable=var_tdr,
        fg_color=ACCENT, hover_color=ACCENT_HOVER
    )
    cb_tdr.pack(anchor="w", pady=4, padx=6)
    ToolTip(cb_tdr, DESCRICAO_TDR)

    # ---------- Bloatware ----------
    ctk.CTkLabel(
        scroll, text="Remover bloatware", text_color=ACCENT,
        font=ctk.CTkFont(size=13, weight="bold")
    ).pack(anchor="w", pady=(18, 6))

    for nome, info in BLOATWARE.items():
        linha = ctk.CTkFrame(scroll, fg_color="transparent")
        linha.pack(fill="x", pady=4, padx=6)

        cb = ctk.CTkCheckBox(linha, text=nome, fg_color=ACCENT, hover_color=ACCENT_HOVER)
        cb.pack(side="left")
        ToolTip(cb, info["descricao"])

        status = ctk.CTkLabel(linha, text="", text_color=TEXT_MUTED, font=ctk.CTkFont(size=12))
        status.pack(side="left", padx=(10, 0))

        checkboxes_bloatware[nome] = (cb, info["id"])
        status_bloatware[nome] = status

    # ---------- Itens de inicialização (detectados no PC do usuário) ----------
    ctk.CTkLabel(
        scroll, text="Itens de inicialização automática", text_color=ACCENT,
        font=ctk.CTkFont(size=13, weight="bold")
    ).pack(anchor="w", pady=(18, 6))

    itens = listar_itens_inicializacao()
    if not itens:
        ctk.CTkLabel(scroll, text="Nenhum item encontrado.", text_color=TEXT_MUTED).pack(anchor="w", padx=6)

    for nome, hive, caminho in itens:
        linha = ctk.CTkFrame(scroll, fg_color="transparent")
        linha.pack(fill="x", pady=4, padx=6)

        cb = ctk.CTkCheckBox(linha, text=nome, fg_color=ACCENT, hover_color=ACCENT_HOVER)
        cb.pack(side="left")
        ToolTip(cb, DESCRICAO_STARTUP)

        status = ctk.CTkLabel(linha, text="", text_color=TEXT_MUTED, font=ctk.CTkFont(size=12))
        status.pack(side="left", padx=(10, 0))

        checkboxes_startup[nome] = (cb, hive, caminho)
        status_startup[nome] = status

    # ---------- Ação do botão ----------
    def ao_clicar_aplicar():
        bloatware_sel = [(nome, aid) for nome, (cb, aid) in checkboxes_bloatware.items() if cb.get()]
        startup_sel = [(nome, hive, caminho) for nome, (cb, hive, caminho) in checkboxes_startup.items() if cb.get()]
        threading.Thread(
            target=aplicar_em_segundo_plano,
            args=(bloatware_sel, startup_sel),
            daemon=True
        ).start()

    def aplicar_em_segundo_plano(bloatware_sel, startup_sel):
        # Cada etapa é (texto_status_antes, função_a_executar, label_de_status_ou_None)
        etapas = []

        if var_telemetria.get():
            etapas.append(("Desativando telemetria...", lambda: desativar_telemetria(janela.log), None))
        if var_energia.get():
            etapas.append(("Ativando alto desempenho...", lambda: ativar_alto_desempenho(janela.log), None))
        if var_limpeza.get():
            etapas.append(("Limpando temporários...", lambda: limpar_temporarios(janela.log), None))
        if var_tdr.get():
            etapas.append(("Ajustando TDR...", lambda: aplicar_tdr_delay(janela.log), None))
        for nome, aid in bloatware_sel:
            etapas.append((None, (lambda n=nome, a=aid: remover_bloatware(n, a, janela.log)), status_bloatware[nome]))
        for nome, hive, caminho in startup_sel:
            etapas.append((None, (lambda n=nome, h=hive, c=caminho: desativar_item_inicializacao(n, h, c, janela.log)), status_startup[nome]))

        if not etapas:
            janela.log("Nenhuma otimização selecionada.")
            return

        total = len(etapas)
        for i, (_texto_geral, funcao, label_status) in enumerate(etapas, start=1):
            if label_status is not None:
                label_status.configure(text="⏳ aplicando...", text_color=ACCENT)
                janela.progresso((i - 0.5) / total)  # anda até a metade do espaço desta etapa

            sucesso = funcao()

            if label_status is not None:
                if sucesso:
                    label_status.configure(text="✅ feito", text_color=VERDE)
                else:
                    label_status.configure(text="❌ erro", text_color=VERMELHO)

            janela.barra.set(i / total)

        janela.log("Otimizações concluídas! Reinicie o PC para todos os efeitos.")
        janela.barra.set(0)

    ctk.CTkButton(
        aba, text="Aplicar otimizações selecionadas", height=38, corner_radius=10,
        fg_color=ACCENT, hover_color=ACCENT_HOVER,
        command=ao_clicar_aplicar
    ).pack(pady=(12, 4))