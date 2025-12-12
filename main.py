# main.py
import tkinter as tk
import os
from app import ControleUI

if __name__ == "__main__":
    root = tk.Tk()

    # --- CONFIGURAÇÃO DO ÍCONE ---
    # Isso define o ícone que aparece na Barra de Tarefas e no canto da janela.
    # Certifique-se de ter um arquivo chamado 'icone.ico' na mesma pasta.
    arquivo_icone = "icone.ico"
    
    if os.path.exists(arquivo_icone):
        try:
            root.iconbitmap(arquivo_icone)
        except Exception as e:
            print(f"Aviso: Não foi possível carregar o ícone. Detalhes: {e}")
    else:
        print("Aviso: Arquivo 'icone.ico' não encontrado. Usando ícone padrão.")

    # Inicia a Interface
    app = ControleUI(root)
    root.mainloop()