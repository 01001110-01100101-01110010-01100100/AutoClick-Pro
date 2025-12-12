# app.py
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time
import json
import random
import keyboard

# Importando nossos módulos
from styles import CORES, FONT_BOLD, FONT_ICON
from components import ModernButton, ModernEntry
from targets import Mira, MiraSwipe

class ControleUI:
    def __init__(self, root):
        self.root = root
        self.root.title("")
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.geometry("60x420+20+100")
        self.root.configure(bg=CORES["bg"])
        
        self.acoes = []
        self.executando = False
        self.visivel = True
        
        self.ciclos_var = tk.StringVar(value="0")
        self.anti_detect_var = tk.BooleanVar(value=False)
        self.tempo_padrao_var = tk.StringVar(value="0.1")

        try:
            keyboard.add_hotkey('F5', self.alternar_play)
            keyboard.add_hotkey('F6', self.alternar_visibilidade)
        except: pass

        self.setup_ui()

    def setup_ui(self):
        # Arrastar
        self.frame_drag = tk.Frame(self.root, bg=CORES["bg"], cursor="fleur")
        self.frame_drag.pack(fill="x", pady=5)
        tk.Label(self.frame_drag, text=":::", bg=CORES["bg"], fg="#555", font=("Arial", 12)).pack()
        self.frame_drag.bind("<ButtonPress-1>", self.start_move)
        self.frame_drag.bind("<B1-Motion>", self.do_move)

        # Botões
        self.btn_play = ModernButton(self.root, text="▶", font=("Segoe UI Symbol", 18), fg=CORES["accent"], command=self.alternar_play)
        self.btn_play.pack(pady=5, fill="x", padx=5)

        ModernButton(self.root, text="➕", font=FONT_ICON, fg=CORES["success"], command=self.add_clique).pack(pady=5, fill="x", padx=5)
        ModernButton(self.root, text="↷", font=("Segoe UI Symbol", 16), fg=CORES["warning"], command=self.add_swipe).pack(pady=5, fill="x", padx=5)
        ModernButton(self.root, text="➖", font=FONT_ICON, fg=CORES["danger"], command=self.remover_ultimo).pack(pady=5, fill="x", padx=5)
        
        ModernButton(self.root, text="⚙", font=("Segoe UI Symbol", 16), fg="#b2bec3", command=self.abrir_settings).pack(pady=15, fill="x", padx=5)
        ModernButton(self.root, text="✕", font=("Arial", 10), fg="#666", bg=CORES["bg"], hover_color="#330000", command=self.root.destroy).pack(side="bottom", pady=10)

    def start_move(self, event): self.x_drag, self.y_drag = event.x, event.y
    def do_move(self, event):
        self.root.geometry(f"+{self.root.winfo_x() + (event.x - self.x_drag)}+{self.root.winfo_y() + (event.y - self.y_drag)}")

    def abrir_settings(self):
        win = tk.Toplevel(self.root)
        win.configure(bg=CORES["bg"])
        win.overrideredirect(True)
        win.geometry("320x450")
        win.attributes('-topmost', True)
        rx, ry = self.root.winfo_x(), self.root.winfo_y()
        win.geometry(f"+{rx + 70}+{ry}")

        title_bar = tk.Frame(win, bg=CORES["btn_bg"], height=30)
        title_bar.pack(fill="x")
        tk.Label(title_bar, text="Configurações", bg=CORES["btn_bg"], fg="white", font=FONT_BOLD).pack(side="left", padx=10)
        ModernButton(title_bar, text="✕", bg=CORES["btn_bg"], hover_color=CORES["danger"], width=4, command=win.destroy).pack(side="right")
        
        def move_win(e): win.geometry(f"+{win.winfo_x() + (e.x - win.x_start)}+{win.winfo_y() + (e.y - win.y_start)}")
        def start_win(e): win.x_start, win.y_start = e.x, e.y
        title_bar.bind("<ButtonPress-1>", start_win)
        title_bar.bind("<B1-Motion>", move_win)

        content = tk.Frame(win, bg=CORES["bg"], padx=15, pady=15)
        content.pack(fill="both", expand=True)

        def criar_grupo(titulo, cor_titulo=CORES["accent"]):
            tk.Label(content, text=titulo, fg=cor_titulo, bg=CORES["bg"], font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(10, 2))
            f = tk.Frame(content, bg=CORES["btn_bg"], padx=10, pady=10)
            f.pack(fill="x")
            return f

        g_seg = criar_grupo("SEGURANÇA", CORES["danger"])
        cb = tk.Checkbutton(g_seg, text="Modo Humano (Anti-Ban)", variable=self.anti_detect_var, 
                            bg=CORES["btn_bg"], fg="white", selectcolor=CORES["bg"], activebackground=CORES["btn_bg"], activeforeground="white")
        cb.pack(anchor="w")
        tk.Label(g_seg, text="Adiciona variações de pixel e tempo.", bg=CORES["btn_bg"], fg="#888", font=("Segoe UI", 8)).pack(anchor="w", padx=20)

        g_auto = criar_grupo("AUTOMAÇÃO")
        tk.Label(g_auto, text="Ciclos (0 = Infinito):", bg=CORES["btn_bg"], fg="white").pack(anchor="w")
        ModernEntry(g_auto, textvariable=self.ciclos_var).pack(fill="x", pady=(2, 8))
        tk.Label(g_auto, text="Espera Padrão (s):", bg=CORES["btn_bg"], fg="white").pack(anchor="w")
        ModernEntry(g_auto, textvariable=self.tempo_padrao_var).pack(fill="x", pady=2)

        g_arq = criar_grupo("ARQUIVOS", "#b2bec3")
        f_btns = tk.Frame(g_arq, bg=CORES["btn_bg"])
        f_btns.pack(fill="x")
        ModernButton(f_btns, text="Exportar .JSON", bg=CORES["bg"], command=self.exportar_json).pack(side="left", fill="x", expand=True, padx=2)
        ModernButton(f_btns, text="Importar .JSON", bg=CORES["bg"], command=self.importar_json).pack(side="left", fill="x", expand=True, padx=2)

        ModernButton(content, text="OK", bg=CORES["accent"], command=win.destroy).pack(side="bottom", fill="x", pady=10)

    def add_clique(self, dados=None):
        n = len(self.acoes) + 1
        x, y = (self.root.winfo_x() + 80, self.root.winfo_y()) if not dados else (dados['x'], dados['y'])
        cfg = dados['config'] if dados else {"tipo": "clique", "acao": "Clique Esquerdo", "espera": float(self.tempo_padrao_var.get())}
        self.acoes.append(Mira(self.root, n, x, y, cfg, self.remover_especifico))

    def add_swipe(self, dados=None):
        n = len(self.acoes) + 1
        x, y = self.root.winfo_x() + 80, self.root.winfo_y()
        cfg = dados['config'] if dados else {"tipo": "swipe", "duracao": 0.5, "espera": float(self.tempo_padrao_var.get())}
        s = MiraSwipe(self.root, n, x, y, x+100, y, cfg, self.remover_especifico) if not dados else \
            MiraSwipe(self.root, n, dados['x1'], dados['y1'], dados['x2'], dados['y2'], cfg, self.remover_especifico)
        self.acoes.append(s)

    def remover_ultimo(self):
        if self.acoes: self.acoes.pop().destruir()

    def remover_especifico(self, item):
        if item in self.acoes:
            item.destruir()
            self.acoes.remove(item)
            self.renumerar()

    def renumerar(self):
        for i, item in enumerate(self.acoes):
            n = i + 1
            if hasattr(item, 'renumerar'): item.renumerar(n)
            else: item.numero = n; item.canvas.itemconfigure(item.texto_id, text=str(n))

    def exportar_json(self):
        f = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if f:
            data = {"tempo_padrao": self.tempo_padrao_var.get(), "ciclos": self.ciclos_var.get(), "anti_detect": self.anti_detect_var.get(), "acoes": [i.get_save_data() for i in self.acoes]}
            with open(f, 'w') as arq: json.dump(data, arq)
            messagebox.showinfo("Sucesso", "Configuração salva!")

    def importar_json(self):
        f = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if f:
            while self.acoes: self.remover_ultimo()
            try:
                with open(f, 'r') as arq:
                    data = json.load(arq)
                    self.tempo_padrao_var.set(data.get("tempo_padrao", "0.1"))
                    self.ciclos_var.set(data.get("ciclos", "0"))
                    for d in data["acoes"]:
                        if d['tipo'] == 'clique': self.add_clique(d)
                        elif d['tipo'] == 'swipe': self.add_swipe(d)
            except Exception as e: messagebox.showerror("Erro", str(e))

    def alternar_play(self):
        if not self.executando:
            self.executando = True
            self.btn_play.config(text="■", fg=CORES["danger"])
            threading.Thread(target=self.loop, daemon=True).start()
        else:
            self.executando = False
            self.btn_play.config(text="▶", fg=CORES["accent"])

    def loop(self):
        try: ciclos = int(self.ciclos_var.get())
        except: ciclos = 0
        count = 0
        while self.executando:
            if ciclos > 0 and count >= ciclos: self.alternar_play(); break
            human = self.anti_detect_var.get()
            for item in self.acoes:
                if not self.executando: break
                item.executar(humanizar=human)
            count += 1
            time.sleep(random.uniform(0.1, 0.3) if human else 0.1)

    def alternar_visibilidade(self):
        self.visivel = not self.visivel
        for item in self.acoes:
            if hasattr(item, 'inicio'):
                if self.visivel: item.inicio.deiconify(); item.fim.deiconify()
                else: item.inicio.withdraw(); item.fim.withdraw()
            else:
                item.deiconify() if self.visivel else item.withdraw()