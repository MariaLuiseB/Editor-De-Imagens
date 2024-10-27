import tkinter as tk
from tkinter import filedialog
import cv2
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image, ImageTk

class EditorImagem(tk.Tk):
    def __init__(self, root): # self chama a classe editor imagem e root chama a janela principal
        # Variaveis pra guardar a imagem original e a imagem atual (com as modificações)
        self.imagem_original = None 
        self.imagem_atual = None
        self.imagem_brilho = None
        self.imagem_negativo = None
        self.imagem_log = None
        self.imagem_exp = None
        self.imagem_referencia = None
        
        # Variaveis de controle
        self.intensidade_brilho = 1
        self.intensidade_contraste = 1

        self.root = root
        self.root.title("Editor de Imagens")

        # Configuração da janela principal
        self.root.columnconfigure(0, weight=1) # weight = 1 ocupa todo o espaço disponível 
        self.root.columnconfigure(1, weight=0) # weight = 0 não ocupa todo o espaço disponível
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=1)
        self.root.minsize(800, 600) # definindo tamanho mínimo 

        # Menu de cima
        self.menu_frame1 = tk.Frame(root, bg="gray")
        self.menu_frame1.grid(row=0, column=0, padx=(0,0), pady=(0,5), sticky="ew", columnspan=2)  # sticky é um grude, ele vai grudar nos dois lados direito e esquerdo (east and west)

        self.botao_abrir = tk.Button(self.menu_frame1, text="Abrir", command=self.abrir_imagem)
        self.botao_abrir.grid(row=0, column=0,pady=8, padx=10)
       
        self.botao_salvar = tk.Button(self.menu_frame1, text="Salvar", command=self.salvar)
        self.botao_salvar.grid(row=0, column=1,pady=8, padx=10)
       
        self.botao_sair = tk.Button(self.menu_frame1, text="Sair", command=self.sair)
        self.botao_sair.grid(row=0, column=2,pady=8, padx=10)

        # Menu do lado
        self.menu_frame2 = tk.Frame(root, bg="gray")
        self.menu_frame2.grid(row=1, column=1, padx=3, pady=(0,0.5), sticky="nsew") 

        self.botao_negativo = tk.Button(self.menu_frame2, text="Filtro Negativo", command=self.aplicar_filtro_neg)
        self.botao_negativo.grid(row=0, column=0,pady=8, padx=10, columnspan=2, sticky="ew")

        self.botao_logaritmico = tk.Button(self.menu_frame2, text="Filtro Logaritmico", command=self.aplicar_filtro_log)
        self.botao_logaritmico.grid(row=1, column=0,pady=8, padx=10, columnspan=2, sticky="ew")

        self.botao_exponencial = tk.Button(self.menu_frame2, text="Filtro Exponencial", command=self.aplicar_filtro_exp)
        self.botao_exponencial.grid(row=2, column=0,pady=8, padx=10, columnspan=2, sticky="ew")
        
        self.frame_transf = tk.Frame(self.menu_frame2, bg="gray")
        self.frame_transf.grid(row=3, column=0, pady=8, padx=10, columnspan=2, sticky="ew")

        self.botao_diminuir_brilho = tk.Button(self.frame_transf, text="Diminuir Brilho", command=self.diminuir_brilho)
        self.botao_diminuir_brilho.grid(row=0, column=0,pady=8, padx=10, sticky="ew")

        self.botao_aumentar_brilho = tk.Button(self.frame_transf, text="Aumentar Brilho", command=self.aumentar_brilho)
        self.botao_aumentar_brilho.grid(row=0, column=1,pady=8, padx=10, sticky="ew")

        self.botao_aplicar_brilho = tk.Button(self.frame_transf, text="Aplicar Brilho", command=self.aplicar_brilho)
        self.botao_aplicar_brilho.grid(row=1, column=0,pady=8, padx=10, columnspan=2, sticky="ew")

        self.botao_diminuir_contraste = tk.Button(self.frame_transf, text="Diminuir Contraste", command=self.diminuir_contraste)
        self.botao_diminuir_contraste.grid(row=2, column=0,pady=8, padx=10)

        self.botao_aumentar_contraste = tk.Button(self.frame_transf, text="Aumentar Contraste", command=self.aumentar_contraste)
        self.botao_aumentar_contraste.grid(row=2, column=1,pady=8, padx=10)
        
        self.botao_aplicar_contraste = tk.Button(self.frame_transf, text="Aplicar Contraste", command=self.aplicar_contraste)
        self.botao_aplicar_contraste.grid(row=3, column=0,pady=8, padx=10, columnspan=2, sticky="ew")
        
        self.botao_aumento = tk.Button(self.menu_frame2, text="Aumentar Imagem", command=self.aplicar_aumento)
        self.botao_aumento.grid(row=4, column=0,pady=8, padx=10, columnspan=2, sticky="ew")

        self.botao_diminuicao = tk.Button(self.menu_frame2, text="Diminuir Imagem", command=self.aplicar_diminuicao)
        self.botao_diminuicao.grid(row=5, column=0,pady=8, padx=10, columnspan=2, sticky="ew")

        self.botao_hist = tk.Button(self.menu_frame2, text="Histograma", command=self.histograma_imagem)
        self.botao_hist.grid(row=6, column=0,pady=8, padx=10, columnspan=2, sticky="ew")

        self.botao_hist_equalizado = tk.Button(self.menu_frame2, text="Histograma Equalizado", command=self.hist_equalizado)
        self.botao_hist_equalizado.grid(row=7, column=0,pady=8, padx=10, columnspan=2, sticky="ew")

        self.botao_box = tk.Button(self.menu_frame2, text="Filtro Box", command=self.filtro_box)
        self.botao_box.grid(row=8, column=0,pady=8, padx=10, columnspan=2, sticky="ew")

        self.botao_gaussiano = tk.Button(self.menu_frame2, text="Filtro Gaussiano", command=self.filtro_gaussiano)
        self.botao_gaussiano.grid(row=9, column=0,pady=8, padx=10, columnspan=2, sticky="ew")

        self.botao_mediana = tk.Button(self.menu_frame2, text="Filtro Mediana", command=self.filtro_mediana)
        self.botao_mediana.grid(row=10, column=0,pady=8, padx=10, columnspan=2, sticky="ew")

        self.botao_laplaciano = tk.Button(self.menu_frame2, text="Filtro Laplaciano", command=self.filtro_agucamento_laplaciano)
        self.botao_laplaciano.grid(row=11, column=0,pady=8, padx=10, columnspan=2, sticky="ew")

        self.botao_sobel = tk.Button(self.menu_frame2, text="Filtro Sobel", command=self.filtro_sobel)
        self.botao_sobel.grid(row=12, column=0,pady=8, padx=10, columnspan=2, sticky="ew")



        # Frame para exibir a imagem
        self.image_frame = tk.Frame(root, bg="white") # fundo branco
        self.image_frame.grid(row=1, column=0, padx=0.8, pady=(0,10), sticky="nsew") # uma matriz dentro da matriz
        self.image_frame.columnconfigure(0, weight=1)
        self.image_frame.rowconfigure(0, weight=1)

        # Canvas para exibir a imagem
        self.canvas = tk.Canvas(self.image_frame, bg="white") 
        self.canvas.grid(row=0, column=0, sticky="nsew")

    def abrir_imagem(self):
        filepath = filedialog.askopenfilename()
        image = cv2.imread(filepath)
        if image is not None:
            self.imagem_original = image
            self.imagem_referencia = image
            self.redimensionar_imagem(image)

    def redimensionar_imagem(self, image):
        canvas_largura = self.canvas.winfo_width() # dimensoes do canva 
        canvas_altura = self.canvas.winfo_height() # dimensoes do canva

        imagem_largura, imagem_altura = image.shape[1], image.shape[0]
        aspect_ratio = imagem_largura / imagem_altura # razao

        if imagem_largura > canvas_largura or imagem_altura > canvas_altura: # se a imagem for maior que o canvas
            if canvas_largura / aspect_ratio > canvas_altura: # se a largura do canvas for maior que a altura
                nova_largura = int(canvas_altura * aspect_ratio) # nova largura = altura do canvas * razao
                nova_altura = canvas_altura # nova altura = altura do canvas
            else:
                nova_largura = canvas_largura # nova largura = largura do canvas
                nova_altura = int(canvas_largura / aspect_ratio) # nova altura = largura do canvas / razao

            image = cv2.resize(image, (nova_largura, nova_altura))

        self.tk_image = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))) # converte a imagem para o formato do tkinter

        self.canvas.delete("all") # deleta a imagem anterior
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image) # cria a nova imagem redimensionada

    def aplicar_filtro_neg(self):
        if self.imagem_original is not None:
            self.imagem_negativo = 255 - self.imagem_original
            self.imagem_atual = self.imagem_negativo
            self.redimensionar_imagem(self.imagem_negativo)

    def aplicar_filtro_log(self):
        if self.imagem_original is not None:
            c = 255.0 / np.log(1 + 255) # c é uma constante para normalizar a imagem logaritmica
            self.imagem_log = c * cv2.log(self.imagem_original.astype(np.float64) + 1.0) #  c * log(1 + imagem_original)
            self.imagem_log = (self.imagem_log - np.min(self.imagem_log)) / (np.max(self.imagem_log) - np.min(self.imagem_log)) * 255.0 # normaliza a imagem
            self.imagem_log = np.uint8(self.imagem_log) # converte a imagem para o formato uint8
            self.imagem_atual = self.imagem_log
            self.redimensionar_imagem(self.imagem_log)
    
    def aplicar_filtro_exp(self):
        self.imagem_exp = cv2.pow(self.imagem_original.astype(np.float32), 2.0) # imagem_exp = imagem_original ^ 2
        self.imagem_exp = (self.imagem_exp - np.min(self.imagem_exp)) / (np.max(self.imagem_exp) - np.min(self.imagem_exp)) * 255.0
        self.imagem_exp = np.uint8(self.imagem_exp)
        self.imagem_atual = self.imagem_exp
        self.redimensionar_imagem(self.imagem_exp)
    

    def aplicar_aumento(self):
        if self.imagem_original is not None:
            self.imagem_zoom = cv2.resize(self.imagem_original, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            self.imagem_atual = self.imagem_zoom
            self.redimensionar_imagem(self.imagem_zoom)

        else:
            print("A imagem não pôde ser processada.")

    def aplicar_diminuicao(self):
        if self.imagem_original is not None:
            self.imagem_zoom = cv2.resize(self.imagem_original, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
            self.imagem_atual = self.imagem_zoom
            self.redimensionar_imagem(self.imagem_zoom)

        else:
            print("A imagem não pôde ser processada.")
    
    def brilho(self, opcao):
        if self.imagem_original is not None:
            if opcao == '+':
                self.intensidade_brilho += 0.5
            elif opcao == '-':
                self.intensidade_brilho -= 0.5
            self.aplicar_brilho()        

    def aumentar_brilho(self):
        self.brilho('+')

    def diminuir_brilho(self):
        self.brilho('-')

    def aplicar_brilho(self):
        if self.imagem_original is not None:
            self.imagem_brilho = cv2.convertScaleAbs(self.imagem_original, beta=self.intensidade_brilho * 10)
            self.imagem_atual = self.imagem_brilho
            self.redimensionar_imagem(self.imagem_brilho)

    def contraste(self, opcao):
        if self.imagem_original is not None:
            if opcao == '+':
                self.intensidade_contraste += 0.2
            elif opcao == '-':
                self.intensidade_contraste -= 0.2
            self.aplicar_contraste()        

    def aumentar_contraste(self):
        self.contraste('+')

    def diminuir_contraste(self):
        self.contraste('-')

    def aplicar_contraste(self):
        if self.imagem_original is not None:
            imagem_contraste = cv2.convertScaleAbs(self.imagem_original, alpha=self.intensidade_contraste)
            self.imagem_atual = imagem_contraste
            self.redimensionar_imagem(imagem_contraste)
    
    def histograma_imagem(self):
        if self.imagem_original is not None:
            self.exibir_hist(self.imagem_original)

    def exibir_hist(self, imagem):
        # Histograma mostrando cada canal de cor
        r, g, b = cv2.split(imagem)

        canal_r = np.histogram(r, bins=256, range=(0, 256)) # bins = número de barras do histograma (0 a 255) = intensidade de cor
        canal_g = np.histogram(g, bins=256, range=(0, 256)) # range = intervalo de valores que o histograma vai mostrar (0 a 256)
        canal_b = np.histogram(b, bins=256, range=(0, 256))

        histograma = np.stack( (canal_r[0], canal_g[0], canal_b[0]), axis=1)
        plt.plot(histograma)
        plt.title("Histograma da Imagem")
        plt.xlabel("Intensidade de Cor")
        plt.ylabel("Quantidade de Pixels")
        plt.show()

    def hist_equalizado(self):
        if self.imagem_original is not None:
            self.imagem_original = cv2.cvtColor(np.array(self.imagem_original), cv2.COLOR_RGB2BGR)
            # self.imagem_original = cv2.cvtColor(self.imagem_original, cv2.COLOR_BGR2GRAY) 
            # Se a imagem for colorida, equalize cada canal separadamente
            canal_r, canal_g, canal_b = cv2.split(self.imagem_original)
            canal_r_equalizado = cv2.equalizeHist(canal_r)
            canal_g_equalizado = cv2.equalizeHist(canal_g)
            canal_b_equalizado = cv2.equalizeHist(canal_b)
            self.imagem_original = cv2.merge((canal_r_equalizado, canal_g_equalizado, canal_b_equalizado))
            self.imagem_original = cv2.cvtColor(self.imagem_original, cv2.COLOR_BGR2RGB)
            
            plt.plot(self.imagem_original[0])
            plt.title("Histograma Equalizado da Imagem")
            plt.xlabel("Intensidade de Cor")
            plt.ylabel("Quantidade de Pixels")
            plt.show()


    def filtro_box(self):
        if self.imagem_original is not None:
            self.imagem_box = cv2.blur(self.imagem_original, (5,5)) # (5,5) = tamanho do kernel
            self.imagem_atual = self.imagem_box
            self.redimensionar_imagem(self.imagem_box)
    
    def filtro_gaussiano(self):
        if self.imagem_original is not None:
            self.imagem_gauss = cv2.GaussianBlur(self.imagem_original, (5,5), 0) # 0 = desvio padrão, ou seja, o filtro calcula o desvio padrão automaticamente
            self.imagem_atual = self.imagem_gauss
            self.redimensionar_imagem(self.imagem_gauss)

    def filtro_mediana(self):
        if self.imagem_original is not None:
            self.imagem_mediana = cv2.medianBlur(self.imagem_original, 5)
            self.imagem_atual = self.imagem_mediana
            self.redimensionar_imagem(self.imagem_mediana)

    def filtro_agucamento_laplaciano(self):
        if self.imagem_original is not None:
            # Passo 1: Suavizar a imagem com o filtro gaussiano
            imagem_suavizada = cv2.GaussianBlur(self.imagem_original, (5, 5), 0)

            # Passo 2: Calcular a Laplaciana da imagem suavizada
            laplaciana = cv2.Laplacian(imagem_suavizada, cv2.CV_64F)

            # Passo 3: Usar a Laplaciana para aguçar a imagem original
            c = -1  # Valor de c para o filtro de aguçamento
            imagem_agucada = self.imagem_original + c * laplaciana
            
            # Normaliza a imagem resultante para valores entre 0 e 255
            imagem_agucada = cv2.normalize(imagem_agucada, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

            self.imagem_original = imagem_agucada
            self.redimensionar_imagem(imagem_agucada)

    def filtro_sobel(self):
        if self.imagem_original is not None:
            # Converte a imagem para tons de cinza
            imagem_tons_de_cinza = cv2.cvtColor(self.imagem_original, cv2.COLOR_BGR2GRAY)

            # Define o kernel Sobel para detecção de bordas horizontais
            sobel_x = np.array([[-1, 0, 1],
                                [-2, 0, 2],
                                [-1, 0, 1]])

            # Aplica a convolução com o kernel Sobel horizontal
            bordas_horizontais = cv2.filter2D(imagem_tons_de_cinza, -1, sobel_x)

            # Define o kernel Sobel para detecção de bordas verticais
            sobel_y = np.array([[-1, -2, -1],
                                [0, 0, 0],
                                [1, 2, 1]])

            # Aplica a convolução com o kernel Sobel vertical
            bordas_verticais = cv2.filter2D(imagem_tons_de_cinza, -1, sobel_y)

            # Calcula o gradiente total da imagem
            gradiente_total = np.sqrt(bordas_horizontais**2 + bordas_verticais**2)

            # Ajusta o limiar para realçar as bordas
            limite = 5
            bordas_realcadas = (gradiente_total > limite).astype(np.uint8) * 255

            # Define a imagem atual como a imagem com bordas realçadas
            self.imagem_atual = bordas_realcadas

            # Redimensiona e exibe a imagem
            self.redimensionar_imagem(bordas_realcadas)

    def salvar(self):
        if self.imagem_atual is not None:
            filepath = filedialog.asksaveasfilename(defaultextension='')
            if filepath:
                cv2.imwrite(filepath, self.imagem_atual)

    def sair(self):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk() # root 
    app = EditorImagem(root) 
    root.mainloop()
