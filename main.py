import os
import sys
import shutil
import zipfile
import re
import ctypes
import threading
import tempfile
import subprocess
import yt_dlp
import vlc
import customtkinter as ctk
import time

# ============================================================
# FUNÇÃO PARA ACHAR O ÍCONE NO .EXE (MAGIA DO PYINSTALLER)
# ============================================================
def get_caminho_icone(nome_arquivo):
    """ Essa função garante que o app ache o ícone mesmo depois de virar .exe """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, nome_arquivo)

# ============================================================
# CONFIGURAÇÕES G4T0XX
# ============================================================
SPOTIFY_EXE = r"C:\Users\PC\AppData\Roaming\Spotify\Spotify.exe"
SPOTIFY_SPA = r"C:\Users\PC\AppData\Roaming\Spotify\Apps\xpui.spa"
UPDATE_FOLDER = r"C:\Users\PC\AppData\Local\Spotify\Update"
UPDATE_EXE = os.path.join(UPDATE_FOLDER, "SpotifyUpdate.exe")

COLOR_BG = "#0f0f0f"
COLOR_BAR = "#181818"
COLOR_ACCENT = "#FF0000"

def is_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

# ============================================================
# INTERFACE PRINCIPAL
# ============================================================
class G4toxxApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # NOME DA JANELA ATUALIZADO
        self.title("SPOTIFY PATCHER - PC EDITION")
        self.geometry("1000x750")
        ctk.set_appearance_mode("dark")
        self.configure(fg_color=COLOR_BG)
        
        # --- APLICANDO A LOGO NA JANELA ---
        try:
            self.iconbitmap(get_caminho_icone("favicon.ico"))
        except:
            pass # Se a imagem não for encontrada no teste, ele não crasha
            
        # Engine VLC
        self.instance = vlc.Instance("--no-video", "--quiet")
        self.player = self.instance.media_player_new()

        # Variáveis da Playlist e Controle
        self.playlist = []
        self.current_song_index = -1
        self.is_slider_dragged = False

        # TÍTULO PRINCIPAL ATUALIZADO
        self.label_main = ctk.CTkLabel(self, text="SPOTIFY PATCHER", font=("Impact", 40), text_color=COLOR_ACCENT)
        self.label_main.pack(pady=10)

        # Abas
        self.tabview = ctk.CTkTabview(self, segmented_button_selected_color=COLOR_ACCENT, segmented_button_unselected_color="#1a1a1a")
        self.tabview.pack(padx=10, pady=5, fill="both", expand=True)
        
        self.tab_player = self.tabview.add("G4T0XX PLAYER (YT)")
        self.tab_patch = self.tabview.add("SPOTIFY OPTIMIZER")

        self.setup_player_ui()
        self.setup_patcher_ui()

        # Atualização do tempo e verificação de fim de música
        self.update_time_loop()

    # ============================================================
    # ABA 1: PLAYER YOUTUBE (NOVA INTERFACE)
    # ============================================================
    def setup_player_ui(self):
        # --- PARTE SUPERIOR (Busca e Listas) ---
        self.top_frame = ctk.CTkFrame(self.tab_player, fg_color="transparent")
        self.top_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Coluna Esquerda: Busca
        self.left_col = ctk.CTkFrame(self.top_frame, fg_color="transparent", width=450)
        self.left_col.pack(side="left", fill="both", expand=True, padx=(0, 10))

        search_frame = ctk.CTkFrame(self.left_col, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 10))
        
        self.entry = ctk.CTkEntry(search_frame, placeholder_text="Pesquise no YouTube...", width=300, border_color="#333")
        self.entry.pack(side="left", padx=(0, 10), fill="x", expand=True)
        
        # O "Login" (Puxar cookies do navegador)
        self.browser_var = ctk.StringVar(value="Nenhum")
        self.browser_combo = ctk.CTkComboBox(search_frame, values=["Nenhum", "chrome", "edge", "brave", "firefox"], variable=self.browser_var, width=100)
        self.browser_combo.pack(side="left", padx=(0, 10))

        ctk.CTkButton(search_frame, text="BUSCAR", fg_color=COLOR_ACCENT, hover_color="#990000", width=100, command=self.start_search_thread).pack(side="left")

        self.status_yt = ctk.CTkLabel(self.left_col, text="Pronto para buscar.", text_color="gray")
        self.status_yt.pack()

        self.results_frame = ctk.CTkScrollableFrame(self.left_col, fg_color="#111", border_width=1, border_color="#222")
        self.results_frame.pack(fill="both", expand=True, pady=5)

        # Coluna Direita: Playlist
        self.right_col = ctk.CTkFrame(self.top_frame, fg_color="#111", border_width=1, border_color="#222", width=350)
        self.right_col.pack(side="right", fill="both", expand=True)

        ctk.CTkLabel(self.right_col, text="FILA DE REPRODUÇÃO", font=("Arial", 14, "bold"), text_color=COLOR_ACCENT).pack(pady=10)
        
        self.playlist_frame = ctk.CTkScrollableFrame(self.right_col, fg_color="transparent")
        self.playlist_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # --- BARRA INFERIOR (Controles) ---
        self.bottom_bar = ctk.CTkFrame(self.tab_player, height=100, fg_color=COLOR_BAR, corner_radius=0)
        self.bottom_bar.pack(side="bottom", fill="x")

        # Info da Música Atual
        self.now_playing_lbl = ctk.CTkLabel(self.bottom_bar, text="Nenhuma música tocando", font=("Arial", 14, "bold"), text_color="white")
        self.now_playing_lbl.pack(pady=(10, 0))

        # Controle de Tempo (Slider interativo)
        time_frame = ctk.CTkFrame(self.bottom_bar, fg_color="transparent")
        time_frame.pack(fill="x", padx=20, pady=5)

        self.time_lbl_current = ctk.CTkLabel(time_frame, text="00:00", text_color="gray", width=40)
        self.time_lbl_current.pack(side="left")

        self.seek_slider = ctk.CTkSlider(time_frame, from_=0, to=100, progress_color=COLOR_ACCENT, button_color="white", button_hover_color=COLOR_ACCENT)
        self.seek_slider.set(0)
        self.seek_slider.pack(side="left", fill="x", expand=True, padx=10)
        # Eventos do mouse para arrastar a barra
        self.seek_slider.bind("<ButtonPress-1>", self.on_slider_press)
        self.seek_slider.bind("<ButtonRelease-1>", self.on_slider_release)

        self.time_lbl_total = ctk.CTkLabel(time_frame, text="00:00", text_color="gray", width=40)
        self.time_lbl_total.pack(side="right")

        # Botões Play/Pause/Skip e Volume
        controls_frame = ctk.CTkFrame(self.bottom_bar, fg_color="transparent")
        controls_frame.pack(pady=(0, 10))

        ctk.CTkButton(controls_frame, text="⏮", width=40, fg_color="transparent", hover_color="#333", font=("Arial", 20), command=self.play_previous).pack(side="left", padx=5)
        self.btn_play = ctk.CTkButton(controls_frame, text="⏸", width=40, fg_color="white", text_color="black", hover_color="#ddd", font=("Arial", 20), command=self.toggle_play)
        self.btn_play.pack(side="left", padx=5)
        ctk.CTkButton(controls_frame, text="⏭", width=40, fg_color="transparent", hover_color="#333", font=("Arial", 20), command=self.play_next).pack(side="left", padx=5)

        ctk.CTkLabel(controls_frame, text="🔊", font=("Arial", 16)).pack(side="left", padx=(30, 5))
        self.volume_slider = ctk.CTkSlider(controls_frame, from_=0, to=100, width=100, progress_color=COLOR_ACCENT, button_color="white", command=self.change_volume)
        self.volume_slider.set(100)
        self.volume_slider.pack(side="left")

    # ============================================================
    # ABA 2: SPOTIFY OPTIMIZER
    # ============================================================
    def setup_patcher_ui(self):
        self.p_console = ctk.CTkTextbox(self.tab_patch, width=650, height=250, fg_color="#0a0a0a", text_color=COLOR_ACCENT, font=("Consolas", 12))
        self.p_console.pack(pady=20)
        self.p_console.insert("0.0", f">>> CAMINHO: {SPOTIFY_EXE}\n>>> STATUS: AGUARDANDO COMANDO")

        self.btn_run = ctk.CTkButton(self.tab_patch, text="EXECUTAR FULL PATCH", fg_color=COLOR_ACCENT, hover_color="#990000", height=50, font=("Arial", 18, "bold"), command=self.start_patch_thread)
        self.btn_run.pack(pady=10)

    def log(self, text):
        self.p_console.insert("end", f"\n[G4T0XX] {text}")
        self.p_console.see("end")

    def start_patch_thread(self):
        threading.Thread(target=self.execute_logic, daemon=True).start()

    def execute_logic(self):
        if not is_admin():
            self.log("ERRO: EXECUTE COMO ADMINISTRADOR!")
            return
        self.log("Encerrando processos do Spotify...")
        subprocess.run(["taskkill", "/F", "/IM", "Spotify.exe", "/T"], capture_output=True, creationflags=0x08000000)

        self.log("Bloqueando atualizações automáticas...")
        try:
            if os.path.exists(UPDATE_EXE): os.remove(UPDATE_EXE)
            os.makedirs(UPDATE_EXE, exist_ok=True)
            self.log("Vacina Anti-Update aplicada.")
        except: self.log("Aviso: Falha ao aplicar vacina de update.")

        self.log("Injetando código no XPUI.SPA...")
        try:
            if not os.path.exists(SPOTIFY_SPA):
                self.log(f"ERRO: Arquivo {SPOTIFY_SPA} não encontrado!")
                return

            with tempfile.TemporaryDirectory() as tmp:
                with zipfile.ZipFile(SPOTIFY_SPA, 'r') as z:
                    z.extract("xpui.js", tmp)
                
                js_p = os.path.join(tmp, "xpui.js")
                with open(js_p, "r", encoding="utf-8") as f:
                    js = f.read()

                js = re.sub(r'adsEnabled:!0', 'adsEnabled:!1', js)
                js = js.replace('productState:"free"', 'productState:"premium"')
                
                with open(js_p, "w", encoding="utf-8") as f:
                    f.write(js)
                with zipfile.ZipFile(SPOTIFY_SPA, 'a') as z:
                    z.write(js_p, "xpui.js")
            
            self.log("PATCH FINALIZADO!")
            self.log("Reiniciando seu Spotify Premium...")
            os.startfile(SPOTIFY_EXE)
        except Exception as e:
            self.log(f"ERRO CRÍTICO: {str(e)}")

    # ============================================================
    # FUNÇÕES DE LÓGICA DO PLAYER (BUSCA E PLAYLIST)
    # ============================================================
    def format_time(self, ms):
        if ms < 0: return "00:00"
        s = ms // 1000
        return f"{s//60:02}:{s%60:02}"

    def on_slider_press(self, event):
        self.is_slider_dragged = True

    def on_slider_release(self, event):
        if self.player:
            val = self.seek_slider.get()
            self.player.set_position(val / 100.0)
        self.is_slider_dragged = False

    def toggle_play(self):
        if not self.player: return
        if self.player.is_playing():
            self.player.pause()
            self.btn_play.configure(text="▶")
        else:
            self.player.play()
            self.btn_play.configure(text="⏸")

    def change_volume(self, value):
        if self.player: self.player.audio_set_volume(int(value))

    def update_time_loop(self):
        try:
            if self.player:
                # Se a música acabou (State 6 = Ended), toca a próxima
                if self.player.get_state() == vlc.State.Ended:
                    self.play_next()

                if self.player.is_playing() and not self.is_slider_dragged:
                    current = self.player.get_time()
                    total = self.player.get_length()
                    
                    self.time_lbl_current.configure(text=self.format_time(current))
                    if total > 0:
                        self.time_lbl_total.configure(text=self.format_time(total))
                        self.seek_slider.set((current / total) * 100)
        except: pass
        self.after(500, self.update_time_loop)

    def start_search_thread(self):
        query = self.entry.get()
        if not query: return
        for widget in self.results_frame.winfo_children(): widget.destroy()
        self.status_yt.configure(text="Buscando no YouTube...", text_color="yellow")
        threading.Thread(target=self.search_yt, args=(query,), daemon=True).start()

    def search_yt(self, query):
        try:
            ydl_opts = {'quiet': True, 'extract_flat': True}
            
            # MAGIA DO LOGIN: Puxa os cookies do navegador escolhido
            browser = self.browser_var.get()
            if browser != "Nenhum":
                ydl_opts['cookiesfrombrowser'] = (browser,)

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch10:{query}", download=False)
                entries = info.get('entries', [])

            for i, entry in enumerate(entries):
                title = entry.get('title', 'Sem Título')
                url = entry.get('url')
                
                row = ctk.CTkFrame(self.results_frame, fg_color="transparent")
                row.pack(fill="x", pady=2, padx=5)
                
                ctk.CTkLabel(row, text=f"{title[:50]}...", anchor="w").pack(side="left", fill="x", expand=True)
                
                # Botão para adicionar à fila
                btn_add = ctk.CTkButton(row, text="+ Fila", width=60, fg_color="#333", hover_color=COLOR_ACCENT, 
                                        command=lambda u=url, t=title: self.add_to_playlist(u, t))
                btn_add.pack(side="right")

            self.status_yt.configure(text="Busca concluída.", text_color="green")
        except Exception as e:
            self.status_yt.configure(text=f"Erro na busca: {str(e)}", text_color="red")

    def add_to_playlist(self, url, title):
        song = {"url": url, "title": title}
        self.playlist.append(song)
        self.update_playlist_ui()
        
        # Se for a primeira música, já dá o play automático
        if len(self.playlist) == 1 and not self.player.is_playing():
            self.current_song_index = 0
            self.start_play_thread(song)

    def update_playlist_ui(self):
        for widget in self.playlist_frame.winfo_children(): widget.destroy()
        for i, song in enumerate(self.playlist):
            color = COLOR_ACCENT if i == self.current_song_index else "white"
            ctk.CTkLabel(self.playlist_frame, text=f"{i+1}. {song['title'][:40]}", text_color=color, anchor="w").pack(fill="x", pady=2)

    def play_next(self):
        if self.current_song_index < len(self.playlist) - 1:
            self.current_song_index += 1
            self.start_play_thread(self.playlist[self.current_song_index])
        else:
            self.player.stop()
            self.now_playing_lbl.configure(text="Fim da Fila")
            self.btn_play.configure(text="▶")

    def play_previous(self):
        if self.current_song_index > 0:
            self.current_song_index -= 1
            self.start_play_thread(self.playlist[self.current_song_index])

    def start_play_thread(self, song):
        self.now_playing_lbl.configure(text=f"Carregando: {song['title'][:40]}...")
        self.update_playlist_ui()
        threading.Thread(target=self.play_audio, args=(song,), daemon=True).start()

    def play_audio(self, song):
        try:
            self.player.stop()
            self.seek_slider.set(0)
            
            ydl_opts = {'format': 'bestaudio/best', 'quiet': True}
            
            # Usa os cookies também na hora de tocar o áudio
            browser = self.browser_var.get()
            if browser != "Nenhum":
                ydl_opts['cookiesfrombrowser'] = (browser,)

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(song['url'], download=False)
                stream_url = info['url']
                
                self.player.set_media(self.instance.media_new(stream_url))
                self.player.play()
                self.btn_play.configure(text="⏸")
                self.now_playing_lbl.configure(text=f"Tocando: {song['title']}")
        except Exception as e:
            self.now_playing_lbl.configure(text="Erro ao carregar música.")

if __name__ == "__main__":
    app = G4toxxApp()
    app.mainloop()