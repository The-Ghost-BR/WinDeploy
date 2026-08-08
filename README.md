# WinDeploy

App com interface gráfica para automatizar a configuração de um Windows recém-formatado: instala programas e aplica otimizações do sistema em poucos cliques.

![Python](https://img.shields.io/badge/python-3.13-blue)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)
[![Download](https://img.shields.io/github/v/release/The-Ghost-BR/WinDeploy?label=Download&style=for-the-badge&color=7C6FF0)](https://github.com/The-Ghost-BR/WinDeploy/releases/latest)

## 📥 Download

**[⬇️ Baixar a versão mais recente do WinDeploy](https://github.com/The-Ghost-BR/WinDeploy/releases/latest)**

Baixe o `WinDeploy.exe` na página de releases e execute — não precisa instalar Python nem nada além disso.

## ✨ Funcionalidades

- **Instalar Programas** — instala programas via [winget](https://learn.microsoft.com/pt-br/windows/package-manager/winget/), organizados por categoria (Básicos, Gamer), com descrição ao passar o mouse e indicador visual de progresso.
- **Otimização** — em um só lugar:
  - Desativar telemetria da Microsoft
  - Ativar plano de energia de alto desempenho
  - Limpar arquivos temporários
  - Ajustar TDR do driver de vídeo (evita crashes em carga pesada)
  - Remover bloatware pré-instalado (seleção individual)
  - Desativar itens de inicialização automática (detectados no próprio PC)

O app pede permissão de Administrador automaticamente e mostra o progresso de cada ação em tempo real, sem travar a interface.

## 🖥️ Requisitos

- Windows 10/11 com [winget](https://learn.microsoft.com/pt-br/windows/package-manager/winget/) instalado (já vem por padrão em instalações atualizadas)
- Para rodar em modo desenvolvimento: Python 3.13

## 🚀 Rodando em modo desenvolvimento

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

## 📦 Compilando para .exe

```powershell
pip install pyinstaller
pyinstaller --onefile --windowed --uac-admin --icon=assets\WinDeploy.ico --name WinDeploy --collect-all customtkinter --add-data "assets;assets" main.py
```

O executável final fica em `dist\WinDeploy.exe`.

## 📁 Estrutura do projeto

```
WinDeploy/
├── main.py                    # Ponto de entrada
├── core/                      # Lógica (instalação, otimização, sistema)
├── dados/                     # Catálogos de programas e bloatware
├── interface/                 # Telas (janela, abas, tooltip)
└── assets/                    # Ícone do app
```