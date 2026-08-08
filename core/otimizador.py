"""
core/otimizador.py
===================
Funções de otimização do Windows. Cada função faz uma coisa só, recebe a
função `log` pra avisar o que está acontecendo, e devolve True/False
dizendo se deu certo - assim a interface consegue mostrar ✅ ou ❌.
"""

import os
import shutil
import subprocess
import winreg

# Faz o Windows não abrir nenhuma janela de terminal ao rodar esses comandos
SEM_JANELA = subprocess.CREATE_NO_WINDOW


def desativar_telemetria(log) -> bool:
    """Desativa a coleta de dados de telemetria da Microsoft."""
    log("Desativando telemetria...")
    try:
        chave = winreg.CreateKeyEx(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Policies\Microsoft\Windows\DataCollection",
            0, winreg.KEY_SET_VALUE
        )
        winreg.SetValueEx(chave, "AllowTelemetry", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(chave)

        subprocess.run(
            ["schtasks", "/Change", "/TN",
             r"\Microsoft\Windows\Application Experience\Microsoft Compatibility Appraiser", "/Disable"],
            capture_output=True, creationflags=SEM_JANELA
        )
        log("OK: Telemetria desativada.")
        return True
    except Exception as e:
        log(f"ERRO ao desativar telemetria: {e}")
        return False


def ativar_alto_desempenho(log) -> bool:
    """Troca o plano de energia do Windows para 'Alto Desempenho'."""
    log("Ativando plano de energia de alto desempenho...")
    try:
        subprocess.run(
            ["powercfg", "-setactive", "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"],
            capture_output=True, creationflags=SEM_JANELA
        )
        log("OK: Plano de alto desempenho ativado.")
        return True
    except Exception as e:
        log(f"ERRO ao ativar plano de energia: {e}")
        return False


def limpar_temporarios(log) -> bool:
    """Apaga arquivos temporários do usuário e do Windows."""
    log("Limpando arquivos temporários...")
    pastas = [os.environ.get("TEMP", ""), r"C:\Windows\Temp"]
    removidos = 0

    try:
        for pasta in pastas:
            if not pasta or not os.path.isdir(pasta):
                continue
            for item in os.listdir(pasta):
                caminho = os.path.join(pasta, item)
                try:
                    if os.path.isfile(caminho) or os.path.islink(caminho):
                        os.unlink(caminho)
                    elif os.path.isdir(caminho):
                        shutil.rmtree(caminho, ignore_errors=True)
                    removidos += 1
                except Exception:
                    pass  # arquivo em uso ou sem permissão - só ignora e segue

        log(f"OK: limpeza concluída ({removidos} itens removidos ou ignorados por estarem em uso).")
        return True
    except Exception as e:
        log(f"ERRO na limpeza de temporários: {e}")
        return False


def aplicar_tdr_delay(log) -> bool:
    """Aumenta o tempo de tolerância do driver de vídeo antes de reiniciar (evita crash em carga pesada)."""
    log("Aplicando ajuste de TDR do driver de vídeo...")
    try:
        chave = winreg.CreateKeyEx(
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers",
            0, winreg.KEY_SET_VALUE
        )
        winreg.SetValueEx(chave, "TdrDelay", 0, winreg.REG_DWORD, 10)
        winreg.SetValueEx(chave, "TdrDdiDelay", 0, winreg.REG_DWORD, 10)
        winreg.CloseKey(chave)
        log("OK: TdrDelay e TdrDdiDelay definidos como 10 (requer reiniciar para valer).")
        return True
    except Exception as e:
        log(f"ERRO ao aplicar TDR delay: {e}")
        return False


def remover_bloatware(nome: str, appx_id: str, log) -> bool:
    """Remove um app pré-instalado (bloatware) usando o PowerShell."""
    log(f"Removendo: {nome}...")
    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             f"Get-AppxPackage -Name '{appx_id}' -AllUsers | Remove-AppxPackage -ErrorAction SilentlyContinue"],
            capture_output=True, timeout=60, creationflags=SEM_JANELA
        )
        log(f"OK: {nome} removido.")
        return True
    except Exception as e:
        log(f"ERRO ao remover {nome}: {e}")
        return False


def listar_itens_inicializacao() -> list:
    """
    Lê os programas que abrem automaticamente com o Windows (chave Run do registro)
    e devolve uma lista de (nome, hive, caminho) pra interface mostrar como checkbox.
    """
    itens = []
    locais = [
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
    ]
    for hive, caminho in locais:
        try:
            chave = winreg.OpenKey(hive, caminho, 0, winreg.KEY_READ)
            i = 0
            while True:
                try:
                    nome, _, _ = winreg.EnumValue(chave, i)
                    itens.append((nome, hive, caminho))
                    i += 1
                except OSError:
                    break
            winreg.CloseKey(chave)
        except Exception:
            pass
    return itens


def desativar_item_inicializacao(nome: str, hive, caminho: str, log) -> bool:
    """Remove um item específico da lista de inicialização automática."""
    try:
        chave = winreg.OpenKey(hive, caminho, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(chave, nome)
        winreg.CloseKey(chave)
        log(f"OK: '{nome}' removido da inicialização.")
        return True
    except Exception as e:
        log(f"ERRO ao remover '{nome}' da inicialização: {e}")
        return False