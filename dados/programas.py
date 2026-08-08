"""
dados/programas.py
===================
Catálogo de programas disponíveis pra instalar.

Cada programa tem:
    "id"        -> o código que o winget usa (descubra com: winget search "nome")
    "descricao" -> texto curto que aparece na dica ao passar o mouse

Pra adicionar um programa novo, copie o formato de um já existente.
"""

PROGRAMAS = {
    "Básicos": {
        "Google Chrome": {
            "id": "Google.Chrome",
            "descricao": "Navegador mais usado do mundo, rápido e com muitas extensões.",
        },
        "Mozilla Firefox": {
            "id": "Mozilla.Firefox",
            "descricao": "Navegador focado em privacidade, alternativa ao Chrome.",
        },
        "Opera GX": {
            "id": "Opera.OperaGX",
            "descricao": "Navegador com tema voltado pra jogos, com limitador de uso de RAM/CPU e integração com Discord/Twitch.",
        },
        "7-Zip": {
            "id": "7zip.7zip",
            "descricao": "Compacta e descompacta arquivos .zip, .rar, .7z e outros.",
        },
        "WinRAR": {
            "id": "RARLab.WinRAR",
            "descricao": "Compactador de arquivos clássico, com suporte forte a .rar.",
        },
        "WhatsApp Desktop": {
            "id": "9NKSQGP7F2NH",
            "descricao": "Versão do WhatsApp pra usar direto no computador.",
        },
    },
    "Gamer": {
        "Steam": {
            "id": "Valve.Steam",
            "descricao": "Loja e launcher de jogos mais popular do PC.",
        },
        "Discord": {
            "id": "Discord.Discord",
            "descricao": "Chat de voz e texto usado por comunidades de jogos.",
        },
        "Epic Games Launcher": {
            "id": "EpicGames.EpicGamesLauncher",
            "descricao": "Launcher da Epic Games (Fortnite e jogos gratuitos semanais).",
        },
        "OBS Studio": {
            "id": "OBSProject.OBSStudio",
            "descricao": "Grava e transmite a tela, usado pra lives e gravação de gameplay.",
        },
        "GeForce Experience": {
            "id": "Nvidia.GeForceExperience",
            "descricao": "App oficial da Nvidia pra atualizar drivers e otimizar jogos.",
        },
        "Battle.net": {
            "id": "Blizzard.BattleNet",
            "descricao": "Launcher da Blizzard (World of Warcraft, Overwatch, Diablo).",
        },
        "MSI Afterburner": {
            "id": "Guru3D.Afterburner",
            "descricao": "Monitora e permite fazer overclock da placa de vídeo.",
        },
    },
}