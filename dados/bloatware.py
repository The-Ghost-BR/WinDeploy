"""
dados/bloatware.py
===================
Catálogo de apps pré-instalados do Windows que podem ser removidos.

Cada item tem:
    "id"        -> nome do pacote AppX (descubra com: Get-AppxPackage | Select Name)
    "descricao" -> texto curto explicando o que é e por que alguém removeria
"""

BLOATWARE = {
    "Cortana": {
        "id": "Microsoft.549981C3F5F10",
        "descricao": "Assistente de voz da Microsoft, pouco usada hoje em dia.",
    },
    "Xbox App": {
        "id": "Microsoft.XboxApp",
        "descricao": "App de gerenciamento do Xbox. Desnecessário se você não joga pela loja da Microsoft.",
    },
    "Xbox Game Overlay": {
        "id": "Microsoft.XboxGamingOverlay",
        "descricao": "Overlay que abre com Win+G. Pode ser removido sem afetar o Steam ou outras lojas.",
    },
    "Xbox Identity Provider": {
        "id": "Microsoft.XboxIdentityProvider",
        "descricao": "Serviço de login usado pelos apps do Xbox.",
    },
    "Xbox Speech To Text": {
        "id": "Microsoft.XboxSpeechToTextOverlay",
        "descricao": "Recurso de transcrição de voz do overlay do Xbox.",
    },
    "Skype": {
        "id": "Microsoft.SkypeApp",
        "descricao": "App de videochamadas antigo da Microsoft, hoje pouco usado.",
    },
    "Mapas do Windows": {
        "id": "Microsoft.WindowsMaps",
        "descricao": "App de mapas offline, raramente usado em desktop.",
    },
    "Clima (Bing Weather)": {
        "id": "Microsoft.BingWeather",
        "descricao": "Widget de previsão do tempo.",
    },
    "Seu Telefone (Phone Link)": {
        "id": "Microsoft.YourPhone",
        "descricao": "Espelha notificações e mensagens do celular Android no PC.",
    },
    "Groove Music": {
        "id": "Microsoft.ZuneMusic",
        "descricao": "Player de música da Microsoft, substituído por Spotify na maioria dos casos.",
    },
    "Filmes e TV": {
        "id": "Microsoft.ZuneVideo",
        "descricao": "Player de vídeo/loja de filmes da Microsoft.",
    },
    "Pessoas": {
        "id": "Microsoft.People",
        "descricao": "App de contatos integrado ao Windows.",
    },
    "Correio e Calendário": {
        "id": "Microsoft.WindowsCommunicationsApps",
        "descricao": "Cliente de e-mail e calendário nativo do Windows.",
    },
    "Dicas do Windows": {
        "id": "Microsoft.Getstarted",
        "descricao": "Tela de dicas que aparece pra usuários novos do Windows.",
    },
    "Feedback Hub": {
        "id": "Microsoft.WindowsFeedbackHub",
        "descricao": "App pra enviar sugestões e relatar problemas à Microsoft.",
    },
    "Central de Realidade Mista": {
        "id": "Microsoft.MixedReality.Portal",
        "descricao": "Necessário só se você tiver um headset de realidade virtual da Microsoft.",
    },
    "3D Builder": {
        "id": "Microsoft.3DBuilder",
        "descricao": "App antigo de modelagem 3D simples, pouco usado.",
    },
    "Clipchamp": {
        "id": "Clipchamp.Clipchamp",
        "descricao": "Editor de vídeo básico que vem pré-instalado no Windows 11.",
    },
    "Anúncios do Sistema": {
        "id": "Microsoft.Advertising.Xaml",
        "descricao": "Componente usado por outros apps pra mostrar anúncios.",
    },
    "Solitaire Collection": {
        "id": "Microsoft.MicrosoftSolitaireCollection",
        "descricao": "Coleção de jogos de cartas pré-instalada.",
    },
    "Office Hub (atalhos de propaganda)": {
        "id": "Microsoft.MicrosoftOfficeHub",
        "descricao": "Tela que sugere baixar o Office, não é o Office em si.",
    },
}