import tkinter as tk
from tkinter import messagebox

def processar():
    valor = entrada.get()
    botao.config(state=tk.DISABLED, text="Processando...")  # Desabilita o botão e altera o texto
    try:
        valor_numerico = float(valor)
        output_text.insert(tk.END, f"Vai começar a ser processado pelo Indice: {valor_numerico}\n")
        janela.after(1000, lambda: adicionar_mensagem("Processando indice 1\n"))
        janela.after(2000, lambda: adicionar_mensagem("Processando indice 2\n"))
        janela.after(3000, lambda: adicionar_mensagem("Processando indice 3\n"))
        janela.after(4000, lambda: adicionar_mensagem("Processando indice 4\n"))
        janela.after(5000, lambda: adicionar_mensagem("Processando indice 5\n"))
        janela.after(6000, lambda: adicionar_mensagem("Processando indice 6\n"))
        janela.after(7000, lambda: adicionar_mensagem("Processando indice 7\n"))
        janela.after(8000, lambda: adicionar_mensagem("Processando indice 8\n"))
        janela.after(9000, lambda: adicionar_mensagem("Processando indice 9\n"))
        janela.after(10000, lambda: adicionar_mensagem("Processando indice 10\n"))
        janela.after(11000, lambda: botao.config(state=tk.NORMAL, text="Processar"))  # Reabilita o botão e altera o texto
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um valor numérico válido.")
        botao.config(state=tk.NORMAL, text="Processar")  # Reabilita o botão em caso de erro

def adicionar_mensagem(mensagem):
    output_text.insert(tk.END, mensagem)
    output_text.see(tk.END)  # Faz a barra de rolagem rolar até o final

# Criação da janela principal
janela = tk.Tk()
janela.title("Sistema Download Automatizado - SDA")
janela.geometry("500x300")  # Ajustando o tamanho da janela para 500x300

# Criação do label de instrução
tk.Label(janela, text="Informe o valor da qual precisa iniciar:").pack(pady=5)

# Criação do campo de entrada
entrada = tk.Entry(janela)
entrada.pack(pady=5)

# Criação do botão "Processar"
botao = tk.Button(janela, text="Processar", command=processar)
botao.pack(pady=5)

# Criação do Text widget para exibir os outputs com barra de rolagem
frame_text = tk.Frame(janela)
frame_text.pack(pady=5)
scrollbar = tk.Scrollbar(frame_text)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
output_text = tk.Text(frame_text, height=10, width=60, yscrollcommand=scrollbar.set)
output_text.pack(side=tk.LEFT)
scrollbar.config(command=output_text.yview)

# Execução da janela
janela.mainloop()
