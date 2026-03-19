<p align="center">
  <img src="favicon.ico" alt="Logo Spotify Patcher & G4T0XX Player" width="180"/>
</p>

<h1 align="center">🎧 SPOTIFY PATCHER & G4T0XX PLAYER 🎧</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge"/>
  <img src="https://img.shields.io/badge/CustomTkinter-1f538d?style=for-the-badge&logo=python&logoColor=white" alt="CustomTkinter Badge"/>
  <img src="https://img.shields.io/badge/VLC_Engine-FF8800?style=for-the-badge&logo=vlcmediaplayer&logoColor=white" alt="VLC Badge"/>
  <img src="https://img.shields.io/badge/Open_Source-4CAF50?style=for-the-badge&logo=open-source-initiative&logoColor=white" alt="Open Source Badge"/>
</p>

<p align="center">
  Uma suíte Open Source poderosa para Windows, dividida em duas ferramentas incríveis: um otimizador para o Spotify Desktop e um player de música independente e ultra leve rodando direto do YouTube.
</p>

<br>

<p align="center">
  <img src="screenshot.png" alt="Interface do G4T0XX Player" width="800"/>
</p>

<br>

---

## ✨ Funcionalidades

### 🟢 SPOTIFY OPTIMIZER (Patcher)
* **Ad-Block Nativo:** Modifica o arquivo `xpui.spa` do Spotify para bloquear anúncios de áudio e visuais.
* **Premium UI:** Desbloqueia a interface visual da versão Premium.
* **Anti-Update:** Aplica uma "vacina" que impede o Spotify de forçar atualizações automáticas, garantindo que o patch dure mais tempo.
* **Automação (1-Click):** Encerra o Spotify, aplica a modificação e reinicia o aplicativo automaticamente.

### 🔴 G4T0XX PLAYER (YouTube via VLC)
* **Busca Integrada:** Pesquise qualquer música ou vídeo do YouTube direto no app.
* **Login Mágico (Sincronização de Cookies):** Extrai automaticamente a sessão do seu navegador (Chrome, Edge, Brave, Firefox) para tocar músicas com restrição de idade ou da sua conta Premium do YouTube.
* **Fila de Reprodução (Playlist):** Adicione várias músicas para tocarem em sequência contínua.
* **Controles Precisos:** Barra de progresso interativa, controle de volume, avançar e retroceder.
* **Performance:** Roda apenas o fluxo de áudio em segundo plano usando a engine do `VLC`, consumindo pouquíssima memória RAM.

---

## ⚠️ Pré-requisitos (MUITO IMPORTANTE)

Para que a suíte funcione perfeitamente no seu computador, você **precisa** ter os seguintes programas instalados:

1. **[VLC Media Player](https://www.videolan.org/vlc/)**: O G4T0XX Player utiliza o motor de áudio do VLC para tocar as músicas do YouTube de forma leve. **Sem ele, o áudio não vai tocar!**
2. **[Spotify Desktop Oficial (.exe)](https://www.spotify.com/br-pt/download/windows/)**: O Patcher **NÃO FUNCIONA** na versão da Microsoft Store. Se você baixou pela loja do Windows, desinstale e baixe a versão oficial no link.

---

## 📥 Como Baixar e Usar (Modo Fácil)

Se você quer apenas usar o programa, não precisa instalar código algum:

1. Acesse a aba **[Releases](https://github.com/G4T0XXPOLIGONAL/SPOTIFY-PATCHER/releases)** aqui no lado direito do GitHub.
2. Baixe o arquivo mais recente: `SPOTIFY_PATCHER.exe`.
3. Dê um duplo clique para abrir.
> **⚠️ Nota:** Para o patch do Spotify funcionar corretamente, é recomendado executar o `.exe` como **Administrador**.

---

## 💻 Para Desenvolvedores (Código-Fonte)

Quer estudar o código ou fazer suas próprias modificações? Siga os passos:

**1. Clone o repositório:**
```bash
git clone [https://github.com/G4T0XXPOLIGONAL/SPOTIFY-PATCHER.git](https://github.com/G4T0XXPOLIGONAL/SPOTIFY-PATCHER.git)
cd SPOTIFY-PATCHER
2. Instale as bibliotecas necessárias:

Bash
pip install customtkinter yt-dlp python-vlc
3. Rode o aplicativo:

Bash
python main.py
🛠️ Avisos e Resolução de Problemas
Conflito com Spicetify: Se você utiliza o Spicetify, o patch do Spotify não encontrará o arquivo xpui.spa. Para usar este patcher, abra o terminal e rode spicetify restore para voltar o Spotify ao formato original antes de aplicar o patch.

⚖️ Aviso Legal
Este projeto foi criado estritamente para fins educacionais e de estudo sobre manipulação de arquivos locais, automação e consumo de APIs de mídia. Os desenvolvedores não se responsabilizam pelo mau uso da ferramenta ou por eventuais violações dos Termos de Serviço das plataformas citadas.

<p align="center"><i>Criado com 💻 e ☕ por <b>G4T0XX</b></i></p>