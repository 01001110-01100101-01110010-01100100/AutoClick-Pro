# targets.py
import tkinter as tk
import pyautogui
import time
import random
from styles import CORES, FONT_MAIN
from components import ModernButton, ModernEntry

class Mira(tk.Toplevel):
    def __init__(self, master, numero, x=100, y=100, config=None, callback_remover=None):
        super().__init__(master)
        self.numero = numero
        self.callback_remover = callback_remover
        self.configuracao = config if config else {"tipo": "clique", "acao": "Clique Esquerdo", "espera": 0.1}

        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self.attributes('-alpha', 0.9)
        self.geometry(f"45x45+{x}+{y}")
        self.attributes('-transparentcolor', '#000001')

        self.canvas = tk.Canvas(self, width=45, height=45, bg="#000001", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_oval(2, 2, 43, 43, fill="#0097e6", outline="#192a56", width=2)
        centro = 22
        self.canvas.create_oval(centro-3, centro-3, centro+3, centro+3, fill="#192a56", outline="")
        self.texto_id = self.canvas.create_text(centro, centro, text=str(numero), fill="white", font=("Segoe UI", 12, "bold"))
        
        self.canvas.bind("<ButtonPress-1>", self.iniciar_movimento)
        self.canvas.bind("<B1-Motion>", self.mover)
        self.canvas.bind("<Button-3>", self.abrir_menu)

    def iniciar_movimento(self, event): self.x_drag, self.y_drag = event.x, event.y
    def mover(self, event):
        self.geometry(f"+{self.winfo_x() + (event.x - self.x_drag)}+{self.winfo_y() + (event.y - self.y_drag)}")

    def abrir_menu(self, event):
        menu = tk.Menu(self, tearoff=0, bg=CORES["bg"], fg=CORES["fg"])
        menu.add_command(label=f"Alvo #{self.numero}", state="disabled")
        menu.add_separator()
        submenu = tk.Menu(menu, tearoff=0, bg=CORES["bg"], fg=CORES["fg"])
        submenu.add_radiobutton(label="Clique Esquerdo", command=lambda: self.configuracao.update({"acao": "Clique Esquerdo"}))
        submenu.add_radiobutton(label="Clique Duplo", command=lambda: self.configuracao.update({"acao": "Clique Duplo"}))
        menu.add_cascade(label="Ação", menu=submenu)
        menu.add_command(label="Definir Tempo...", command=self.pedir_espera)
        menu.add_separator()
        menu.add_command(label="Remover", command=lambda: self.callback_remover(self))
        menu.post(event.x_root, event.y_root)

    def pedir_espera(self):
        win = tk.Toplevel(self)
        win.configure(bg=CORES["bg"])
        win.overrideredirect(True)
        win.geometry("200x120+{}+{}".format(self.winfo_x(), self.winfo_y()))
        win.attributes('-topmost', True)
        
        tk.Frame(win, bg=CORES["accent"], height=2).pack(fill="x")
        tk.Label(win, text="Espera (segundos):", bg=CORES["bg"], fg=CORES["fg"], font=FONT_MAIN).pack(pady=10)
        e = ModernEntry(win, justify="center")
        e.insert(0, str(self.configuracao["espera"]))
        e.pack(pady=5, padx=20, fill="x")
        
        frame_b = tk.Frame(win, bg=CORES["bg"])
        frame_b.pack(pady=10)
        ModernButton(frame_b, text="Salvar", bg=CORES["accent"], command=lambda: [self.configuracao.update({"espera": float(e.get())}), win.destroy()]).pack(side="left", padx=5)
        ModernButton(frame_b, text="Cancelar", bg=CORES["btn_bg"], command=win.destroy).pack(side="left", padx=5)

    def executar(self, humanizar=False):
        x, y = self.winfo_x() + 22, self.winfo_y() + 22
        tempo = self.configuracao["espera"]
        if humanizar:
            x += random.randint(-2, 2); y += random.randint(-2, 2)
            tempo *= random.uniform(0.8, 1.2)
        self.attributes('-alpha', 0.0); time.sleep(0.05)
        try:
            acao = self.configuracao["acao"]
            if acao == "Clique Esquerdo": pyautogui.click(x, y)
            elif acao == "Clique Duplo": pyautogui.doubleClick(x, y)
        except: pass
        self.attributes('-alpha', 0.9); time.sleep(tempo)
    def get_save_data(self): return {"tipo": "clique", "x": self.winfo_x(), "y": self.winfo_y(), "config": self.configuracao}
    def destruir(self): self.destroy()

class MiraSwipe:
    def __init__(self, master, numero, x1=100, y1=100, x2=200, y2=100, config=None, callback_remover=None):
        self.master = master; self.numero = numero; self.callback_remover = callback_remover
        self.configuracao = config if config else {"tipo": "swipe", "duracao": 0.5, "espera": 0.5}
        self.inicio = self._criar_bola(x1, y1, "#2ecc71", "S")
        self.fim = self._criar_bola(x2, y2, "#e74c3c", "E")

    def _criar_bola(self, x, y, cor, letra):
        win = tk.Toplevel(self.master)
        win.overrideredirect(True); win.attributes('-topmost', True); win.attributes('-alpha', 0.9)
        win.attributes('-transparentcolor', '#000001'); win.geometry(f"45x45+{x}+{y}")
        canvas = tk.Canvas(win, width=45, height=45, bg="#000001", highlightthickness=0)
        canvas.pack()
        canvas.create_oval(2, 2, 43, 43, fill=cor, outline="#192a56", width=2)
        centro = 22
        canvas.create_oval(centro-3, centro-3, centro+3, centro+3, fill="#192a56", outline="")
        tid = canvas.create_text(centro, centro, text=f"{self.numero}{letra}", fill="white", font=("Segoe UI", 11, "bold"))
        win.x_drag, win.y_drag = 0, 0
        def start(e): win.x_drag, win.y_drag = e.x, e.y
        def move(e): win.geometry(f"+{win.winfo_x() + (e.x - win.x_drag)}+{win.winfo_y() + (e.y - win.y_drag)}")
        def menu(e): 
            m = tk.Menu(win, tearoff=0, bg=CORES["bg"], fg=CORES["fg"])
            m.add_command(label="Remover", command=lambda: self.callback_remover(self))
            m.post(e.x_root, e.y_root)
        canvas.bind("<ButtonPress-1>", start); canvas.bind("<B1-Motion>", move); canvas.bind("<Button-3>", menu)
        win.tid = tid; win.cv = canvas
        return win
    
    def executar(self, humanizar=False):
        x1, y1 = self.inicio.winfo_x()+22, self.inicio.winfo_y()+22
        x2, y2 = self.fim.winfo_x()+22, self.fim.winfo_y()+22
        d = self.configuracao["duracao"]
        if humanizar: d *= random.uniform(0.9, 1.1); x1 += random.randint(-2,2); x2 += random.randint(-2,2)
        self.inicio.attributes('-alpha', 0); self.fim.attributes('-alpha', 0); time.sleep(0.1)
        try: pyautogui.moveTo(x1, y1); pyautogui.dragTo(x2, y2, duration=d, button='left', tween=pyautogui.easeOutQuad if humanizar else pyautogui.linear)
        except: pass
        self.inicio.attributes('-alpha', 0.9); self.fim.attributes('-alpha', 0.9); time.sleep(self.configuracao["espera"])
    def renumerar(self, n):
        self.numero = n
        self.inicio.cv.itemconfigure(self.inicio.tid, text=f"{n}S"); self.fim.cv.itemconfigure(self.fim.tid, text=f"{n}E")
    def get_save_data(self): return {"tipo": "swipe", "x1": self.inicio.winfo_x(), "y1": self.inicio.winfo_y(), "x2": self.fim.winfo_x(), "y2": self.fim.winfo_y(), "config": self.configuracao}
    def destruir(self): self.inicio.destroy(); self.fim.destroy()