"""
core/sistema.py
================
Funções genéricas relacionadas ao sistema operacional: elevação de
administrador, efeito visual da janela (Mica/Acrylic), e localização de
arquivos internos do app (como o ícone) tanto em desenvolvimento quanto
já compilado em .exe.
"""

import ctypes
import os
import sys


def is_admin() -> bool:
    """Retorna True se o programa já está rodando como Administrador."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def relaunch_as_admin():
    """Reabre o programa pedindo permissão de Administrador (mostra o UAC)."""
    params = " ".join(f'"{a}"' for a in sys.argv)
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
    sys.exit(0)


def aplicar_efeito_janela(janela) -> str:
    """
    Tenta deixar a janela com um efeito translúcido nativo do Windows.
    Primeiro tenta o Mica (visual do Windows 11); se não der certo (ex: o
    usuário está no Windows 10), cai automaticamente pro Acrylic (blur),
    que tem suporte mais amplo. Se nenhum dos dois funcionar, ignora e o
    app continua normal, só sem o efeito.

    Retorna qual efeito foi aplicado: "mica", "acrylic" ou "nenhum".
    """
    try:
        import pywinstyles

        try:
            pywinstyles.apply_style(janela, "mica")
            return "mica"
        except Exception:
            pywinstyles.apply_style(janela, "acrylic")
            return "acrylic"
    except Exception:
        return "nenhum"


def caminho_recurso(caminho_relativo: str) -> str:
    """
    Devolve o caminho correto de um arquivo interno do app (como o ícone),
    funcionando tanto quando rodamos com 'python main.py' (modo
    desenvolvimento) quanto depois de compilado em .exe pelo PyInstaller
    (que extrai os arquivos numa pasta temporária diferente a cada vez).
    """
    if hasattr(sys, "_MEIPASS"):
        # Rodando como .exe compilado - os arquivos ficam numa pasta temporária
        base = sys._MEIPASS
    else:
        # Rodando com "python main.py" - usa a pasta raiz do projeto
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(base, caminho_relativo)