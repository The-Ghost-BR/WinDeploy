"""
core/instalador.py
===================
Funções relacionadas à instalação de programas via winget: verificar se
ele existe, tentar mantê-lo atualizado, e instalar um programa específico.
"""

import subprocess

# Faz o Windows não abrir nenhuma janela de terminal ao rodar esses comandos
SEM_JANELA = subprocess.CREATE_NO_WINDOW


def verificar_winget() -> bool:
    """Retorna True se o winget está instalado e respondendo nesse PC."""
    try:
        subprocess.run(["winget", "--version"], capture_output=True, timeout=10, creationflags=SEM_JANELA)
        return True
    except Exception:
        return False


def atualizar_winget(log) -> None:
    """
    Tenta atualizar o próprio winget (via o pacote 'App Installer') antes de
    começar a instalar qualquer coisa, pra evitar erros por versão antiga.
    Só roda se o winget já existir - não instala ele do zero.
    """
    log("Verificando atualizações do winget...")
    try:
        subprocess.run(
            ["winget", "upgrade", "--id", "Microsoft.AppInstaller",
             "--silent", "--accept-source-agreements", "--accept-package-agreements"],
            capture_output=True, timeout=120, creationflags=SEM_JANELA
        )
        log("OK: winget verificado/atualizado.")
    except Exception:
        log("Aviso: não foi possível verificar atualização do winget, seguindo mesmo assim.")


def instalar_programa(nome: str, winget_id: str, log) -> bool:
    """
    Instala um programa usando o winget, em modo silencioso.
    Retorna True se deu certo, False se deu erro.
    """
    log(f"Instalando: {nome}...")
    try:
        subprocess.run(
            [
                "winget", "install",
                "--id", winget_id,
                "--silent",
                "--accept-source-agreements",
                "--accept-package-agreements",
                "-e",
            ],
            capture_output=True,
            timeout=600,
            creationflags=SEM_JANELA,
        )
        log(f"OK: {nome} instalado.")
        return True
    except Exception as e:
        log(f"ERRO ao instalar {nome}: {e}")
        return False