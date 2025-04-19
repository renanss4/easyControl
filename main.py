import tkinter as tk

def main():
    # Cria a janela principal
    root = tk.Tk()
    root.title("EasyControl - Sistema de Férias")
    root.geometry("300x200")  # Largura x Altura

    # Adiciona um texto de exemplo
    label = tk.Label(root, text="Hello, Tkinter!", font=("Arial", 14))
    label.pack(pady=50)

    # Inicia o loop principal da interface
    root.mainloop()

if __name__ == "__main__":
    main()
