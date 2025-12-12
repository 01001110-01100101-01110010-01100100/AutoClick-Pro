# AutoClick Pro 🎯

> Uma ferramenta de automação profissional para Windows — moderna, indetectável e **Open Source**.

![Python](https://img.shields.io/badge/Made%20with-Python-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![License](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge\&logo=windows\&logoColor=white)

---

## 📋 Sobre o Projeto

O **AutoClick Pro** é um software de automação de cliques e swipes feito em Python.
Diferente de scripts comuns, ele possui uma **Interface Profissional (Dark/Flat)**, focada em usabilidade, precisão e segurança.

O sistema também possui um **Modo Humano (Anti-Ban)** que aplica variações reais de posição e tempo para simular um comportamento humano e reduzir detecção.

---

## ✨ Funcionalidades

* **Interface Moderna:** Design escuro, minimalista e sem bordas padrão do Windows.
* **Alvos Visuais Inteligentes:** Miras numeradas “Target Style” com excelente precisão.
* **Ações Suportadas:**

  * Clique esquerdo
  * Duplo clique
  * Swipes (arrastar)
* **🛡️ Modo Humano (Anti-Detecção):**

  * Variação randômica de pixel
  * Atrasos adaptativos
* **Memória Automática:** Suas configurações permanecem salvas.
* **Sistema de Arquivos:**

  * Exportar scripts
  * Importar scripts (JSON)
* **Atalhos Globais:**

  * `F5`: Iniciar / Parar
  * `F6`: Ocultar / Mostrar interface

---

## 📂 Estrutura do Projeto (Source)

```
AutoClickPro/
│
├── main.py           # Arquivo Principal (Entry Point)
├── app.py            # Lógica central e interface do menu
├── components.py     # Componentes visuais (botões, inputs customizados)
├── targets.py        # Classes das miras (alvos, swipes)
├── styles.py         # Paleta de cores e fontes (Dark Theme)
│
├── icone.ico         # Ícone oficial do aplicativo
├── Licenca.txt       # Licença usada no instalador
└── requirements.txt  # Dependências do projeto
```

---

## 🛠️ Como Executar (Modo Dev)

Clone o repositório:

```bash
git clone https://github.com/01001110-01100101-01110010-01100100/AutoClick-Pro.git
cd AutoClickPro
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute o projeto:

```bash
python main.py
```

---

## 📦 Como Gerar o Executável (Build)

### **1️⃣ Criar o Executável (.exe) com PyInstaller**

Como o arquivo `icone.ico` já está no projeto, execute:

```bash
pyinstaller --noconsole --onefile --icon=icone.ico --name="AutoClickPro" main.py
```

O executável final estará em:

```
dist/AutoClickPro.exe
```

---

### **2️⃣ Criar o Instalador (Opcional)**

Para gerar um instalador profissional (`setup.exe`) usando Inno Setup:

1. Instale **Inno Setup**.
2. Crie um novo script usando o Wizard.
3. Aponte para o `AutoClickPro.exe` da pasta *dist/*.
4. No campo de licença, selecione `Licenca.txt`.
5. Compile para gerar o instalador final.

---

## ⚖️ Licença

Este projeto é licenciado sob:

### **Creative Commons CC BY-NC-SA 4.0**

**Você pode:**

* ✔️ Baixar
* ✔️ Estudar
* ✔️ Modificar
* ✔️ Compartilhar versões derivadas

**Você NÃO pode:**

* ❌ Vender este software
* ❌ Monetizar direta ou indiretamente
* ❌ Comercializar versões modificadas

---

Feito com carinho em 🐍 Python.
