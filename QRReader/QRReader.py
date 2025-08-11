import tkinter as tk
from tkinter import messagebox
from PIL import ImageGrab, Image
from pyzbar.pyzbar import decode
import webbrowser
import pyperclip  # Para copiar texto
import sys
import os


def resource_path(relative_path):
    """ Get absolute path to resource """
    try:
        # PyInstaller cria uma pasta temporária no _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class QRCodeReaderApp:
    def __init__(self, master):
        self.master = master
        self.master.iconbitmap(resource_path("src/img/icon.ico"))
        self.master.title("Leitor de QR Code")
        self.master.geometry("300x150")
        self.master.configure(bg="#2E2E2E")

        # Botão "Iniciar Leitura" (estilo moderno)
        self.btn_iniciar = tk.Button(
            master,
            text="Iniciar Leitura",
            command=self.iniciar_leitura,
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            activebackground="#45a049",
            relief="flat"
        )
        self.btn_iniciar.pack(pady=40)

    def iniciar_leitura(self):
        self.master.iconify()  # Minimiza a janela principal

        # Janela de seleção de área (fundo preto dinâmico)
        selecionador = tk.Toplevel()
        selecionador.attributes("-fullscreen", True)
        selecionador.attributes("-alpha", 0.5)
        selecionador.configure(bg="black")
        canvas = tk.Canvas(selecionador, cursor="cross", bg="black", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        # Variáveis para a seleção
        self.start_x, self.start_y = None, None
        self.rect = None

        def on_press(event):
            self.start_x, self.start_y = event.x, event.y
            self.rect = canvas.create_rectangle(
                self.start_x, self.start_y, self.start_x, self.start_y,
                outline="#FF0000", width=2, dash=(5, 5)
            )

        def on_drag(event):
            canvas.coords(
                self.rect,
                self.start_x, self.start_y,
                event.x, event.y
            )

        def on_release(event):
            x1, y1 = self.start_x, self.start_y
            x2, y2 = event.x, event.y
            x1, x2 = sorted([x1, x2])
            y1, y2 = sorted([y1, y2])

            screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            selecionador.destroy()
            self.processar_imagem(screenshot)

        canvas.bind("<ButtonPress-1>", on_press)
        canvas.bind("<B1-Motion>", on_drag)
        canvas.bind("<ButtonRelease-1>", on_release)

    def processar_imagem(self, imagem):
        try:
            resultado = decode(imagem)
            if resultado:
                texto = resultado[0].data.decode()
                self.mostrar_resultado(texto)
            else:
                messagebox.showerror("Erro", "Nenhum QR Code encontrado!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao ler QR Code: {e}")
        finally:
            self.master.deiconify()

    def mostrar_resultado(self, texto):
        result_window = tk.Toplevel(self.master)
        result_window.title("Resultado")
        result_window.geometry("450x200")
        result_window.configure(bg="#2E2E2E")

        # Frame principal
        frame = tk.Frame(result_window, bg="#2E2E2E")
        frame.pack(pady=20)

        # Label com o texto
        tk.Label(
            frame,
            text="Conteúdo encontrado:",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#2E2E2E"
        ).pack()

        tk.Label(
            frame,
            text=texto,
            font=("Arial", 10),
            wraplength=400,
            fg="#FFFFFF",
            bg="#3E3E3E",
            padx=10,
            pady=10
        ).pack(pady=10)

        # Frame para botões
        btn_frame = tk.Frame(frame, bg="#2E2E2E")
        btn_frame.pack(pady=10)

        # Botão "Copiar Texto"
        tk.Button(
            btn_frame,
            text="Copiar Texto",
            command=lambda: self.copiar_texto(texto),
            font=("Arial", 10),
            bg="#555555",
            fg="white",
            activebackground="#666666",
            relief="flat"
        ).pack(side="left", padx=5)

        # Botão "Abrir Link" (só aparece se for um link válido)
        if texto.startswith(("http://", "https://")):
            tk.Button(
                btn_frame,
                text="Abrir Link",
                command=lambda: webbrowser.open(texto),
                font=("Arial", 10),
                bg="#2196F3",
                fg="white",
                activebackground="#1E88E5",
                relief="flat"
            ).pack(side="left", padx=5)

    def copiar_texto(self, texto):
        pyperclip.copy(texto)
        messagebox.showinfo("Sucesso", "Texto copiado para a área de transferência!")

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeReaderApp(root)
    root.mainloop()