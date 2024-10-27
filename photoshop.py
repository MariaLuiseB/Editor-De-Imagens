import math
import tkinter as tk
from tkinter import filedialog
import cv2
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image, ImageTk
from tkinter import Scrollbar


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
        self.valor_input_kernel = None
        
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
        self.botao_abrir.grid(row=0, column=0,pady=6, padx=10)
       
        self.botao_salvar = tk.Button(self.menu_frame1, text="Salvar", command=self.salvar)
        self.botao_salvar.grid(row=0, column=1,pady=6, padx=10)
       
        self.botao_sair = tk.Button(self.menu_frame1, text="Sair", command=self.sair)
        self.botao_sair.grid(row=0, column=2,pady=6, padx=10)

        # Menu do lado
        self.menu_frame2 = tk.Frame(root, bg="gray")
        self.menu_frame2.grid(row=1, column=1, padx=3, pady=(0,0.5), sticky="nsew") 

        self.botao_negativo = tk.Button(self.menu_frame2, text="Filtro Negativo", command=self.filtro_negativo)
        self.botao_negativo.grid(row=0, column=0,pady=6, padx=10, columnspan=2, sticky="ew")

        self.botao_logaritmico = tk.Button(self.menu_frame2, text="Filtro Logaritmico", command=self.filtro_logaritmico)
        self.botao_logaritmico.grid(row=1, column=0,pady=6, padx=10, columnspan=2, sticky="ew")

        self.botao_exponencial = tk.Button(self.menu_frame2, text="Filtro Exponencial", command=self.filtro_exponencial)
        self.botao_exponencial.grid(row=2, column=0,pady=6, padx=10, columnspan=2, sticky="ew")
        
        self.frame_transf = tk.Frame(self.menu_frame2, bg="gray")
        self.frame_transf.grid(row=3, column=0, pady=6, padx=10, columnspan=2, sticky="ew")

        self.botao_diminuir_brilho = tk.Button(self.frame_transf, text="Diminuir Brilho", command=self.diminuir_brilho)
        self.botao_diminuir_brilho.grid(row=0, column=0,pady=6, padx=(0,2), sticky="ew")

        self.botao_aumentar_brilho = tk.Button(self.frame_transf, text="Aumentar Brilho", command=self.aumentar_brilho)
        self.botao_aumentar_brilho.grid(row=0, column=1,pady=6, padx=(2,0), sticky="ew")

        self.botao_aplicar_brilho = tk.Button(self.frame_transf, text="Aplicar Brilho", command=self.aplicar_brilho)
        self.botao_aplicar_brilho.grid(row=1, column=0,pady=6, padx=0, columnspan=2, sticky="ew")

        self.botao_diminuir_contraste = tk.Button(self.frame_transf, text="Diminuir Contraste", command=self.diminuir_contraste)
        self.botao_diminuir_contraste.grid(row=2, column=0,pady=6, padx=(0,2))

        self.botao_aumentar_contraste = tk.Button(self.frame_transf, text="Aumentar Contraste", command=self.aumentar_contraste)
        self.botao_aumentar_contraste.grid(row=2, column=1,pady=6, padx=(2,0))
        
        self.botao_aplicar_contraste = tk.Button(self.frame_transf, text="Aplicar Contraste", command=self.aplicar_contraste)
        self.botao_aplicar_contraste.grid(row=3, column=0,pady=6, padx=0, columnspan=2, sticky="ew")
        
        self.botao_aumento = tk.Button(self.menu_frame2, text="Aumentar Imagem", command=self.aplicar_aumento)
        self.botao_aumento.grid(row=4, column=0,pady=6, padx=10, columnspan=2, sticky="ew")

        self.botao_diminuicao = tk.Button(self.menu_frame2, text="Diminuir Imagem", command=self.aplicar_diminuicao)
        self.botao_diminuicao.grid(row=5, column=0,pady=6, padx=10, columnspan=2, sticky="ew")

        self.botao_hist = tk.Button(self.menu_frame2, text="Histograma", command=self.histograma)
        self.botao_hist.grid(row=6, column=0,pady=6, padx=10, columnspan=2, sticky="ew")

        self.botao_histograma_equalizado = tk.Button(self.menu_frame2, text="Histograma Equalizado", command=self.histograma_equalizado)
        self.botao_histograma_equalizado.grid(row=7, column=0,pady=6, padx=10, columnspan=2, sticky="ew")

        self.botao_histograma_especificacao = tk.Button(self.menu_frame2, text="Histograma de Especificacao", command=self.histograma_especificacao)
        self.botao_histograma_especificacao.grid(row=8, column=0,pady=6, padx=10, columnspan=2, sticky="ew")

        self.botao_box = tk.Button(self.menu_frame2, text="Filtro Box", command=self.filtro_box)
        self.botao_box.grid(row=9, column=0,pady=6, padx=10, sticky="ew")
        self.input_box = tk.Entry(self.menu_frame2, width=1, font=("Arial", 14))
        self.input_box.grid(row=9, column=1,pady=6, padx=10, sticky="ew")

        self.botao_gaussiano = tk.Button(self.menu_frame2, text="Filtro Gaussiano", command=self.filtro_gaussiano)
        self.botao_gaussiano.grid(row=10, column=0,pady=6, padx=10, sticky="ew")
        self.input_gaussiano = tk.Entry(self.menu_frame2, width=1, font=("Arial", 14))
        self.input_gaussiano.grid(row=10, column=1,pady=6, padx=10, sticky="ew")

        self.botao_mediana = tk.Button(self.menu_frame2, text="Filtro Mediana", command=self.filtro_mediana)
        self.botao_mediana.grid(row=11, column=0,pady=6, padx=10, sticky="ew")
        self.input_mediana = tk.Entry(self.menu_frame2, width=1, font=("Arial", 14))
        self.input_mediana.grid(row=11, column=1,pady=6, padx=10, sticky="ew")

        self.botao_laplaciano = tk.Button(self.menu_frame2, text="Filtro Laplaciano", command=self.filtro_laplaciano)
        self.botao_laplaciano.grid(row=12, column=0,pady=6, padx=10, sticky="ew")
        self.input_laplaciano = tk.Entry(self.menu_frame2, width=1, font=("Arial", 14))
        self.input_laplaciano.grid(row=12, column=1,pady=6, padx=10, sticky="ew")

        self.botao_sobel = tk.Button(self.menu_frame2, text="Filtro Sobel", command=self.filtro_sobel)
        self.botao_sobel.grid(row=13, column=0,pady=6, padx=10, sticky="ew")
        self.input_sobel = tk.Entry(self.menu_frame2, width=1, font=("Arial", 12))
        self.input_sobel.grid(row=13, column=1,pady=6, padx=10, sticky="ew")

        self.botao_limiarizacao = tk.Button(self.menu_frame2, text="Filtro Limiarização", command=self.filtro_limiarizacao)
        self.botao_limiarizacao.grid(row=14, column=0,pady=6, padx=10, columnspan=2, sticky="ew")

        self.botao_canny = tk.Button(self.menu_frame2, text="Filtro Canny", command=self.filtro_canny)
        self.botao_canny.grid(row=14, column=0,pady=6, padx=10, columnspan=2, sticky="ew")

        self.botao_hough = tk.Button(self.menu_frame2, text="Filtro Hough", command=self.filtro_hough)
        self.botao_hough.grid(row=15, column=0,pady=6, padx=10, columnspan=2, sticky="ew")

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


    def salvar(self):
        if self.imagem_atual is not None:
            filepath = filedialog.asksaveasfilename(defaultextension='') # salva a imagem com formato padrão que é o formato da imagem original
            if filepath:
                cv2.imwrite(filepath, self.imagem_atual)
        else:
            self.aviso()

    def sair(self):
        self.root.quit()

    
    def aviso(self):
        self.aviso_window = tk.Toplevel(self.root)  # Usar um nome diferente para a instância da janela de aviso
        self.aviso_window.title("Aviso")
        self.aviso_window.columnconfigure(0, weight=1)
        self.aviso_window.rowconfigure(0, weight=1)
        self.aviso_window.minsize(300, 100)
        self.aviso_window.maxsize(300, 100)
        self.aviso_window.resizable(False, False)
        self.aviso_window.grab_set()
        self.aviso_window.focus_set()
        self.aviso_window.transient(self.root)
        self.aviso_label = tk.Label(self.aviso_window, text="Por favor insira uma imagem.")
        self.aviso_label.grid(row=0, column=0, padx=10, pady=10)
        self.aviso_button = tk.Button(self.aviso_window, text="OK", command=self.aviso_window.destroy)  # Usar self.aviso_window.destroy ao invés de self.aviso.destroy
        self.aviso_button.grid(row=1, column=0, padx=10, pady=10)

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
        self.canvas.image = self.tk_image # atualiza a imagem atual
        


    def filtro_negativo(self):
        if self.imagem_original is not None:
            # Subtrai a imagem original de 255 para obter o negativo
            # Se ela for branca (255), o negativo vai ser preto (0)
            # Se ela for preta (0), o negativo vai ser branco (255)
            self.imagem_negativo = 255 - self.imagem_original
            # self.imagem_atual = self.imagem_negativo
            self.redimensionar_imagem(self.imagem_negativo)
        else:
            # Janela que avisa que não tem imagem
            self.aviso()



    def filtro_logaritmico(self):
        if self.imagem_original is not None:
            c = 255.0 / np.log(1 + 255) # c é uma constante para normalizar a imagem logaritmica
            self.imagem_log = c * cv2.log(self.imagem_original.astype(np.float64) + 1.0) #  c * log(1 + imagem_original)
            self.imagem_log = (self.imagem_log - np.min(self.imagem_log)) / (np.max(self.imagem_log) - np.min(self.imagem_log)) * 255.0 # normaliza a imagem
            self.imagem_log = np.uint8(self.imagem_log) # converte a imagem para o formato uint8
            self.imagem_atual = self.imagem_log
            self.redimensionar_imagem(self.imagem_log)
        else:
            # Janela que avisa que não tem imagem
            self.aviso()



    def filtro_exponencial(self):
        if self.imagem_original is not None:
            self.imagem_exp = cv2.pow(self.imagem_original.astype(np.float32), 2.0) # imagem_exp = imagem_original ^ 2
            self.imagem_exp = (self.imagem_exp - np.min(self.imagem_exp)) / (np.max(self.imagem_exp) - np.min(self.imagem_exp)) * 255.0
            self.imagem_exp = np.uint8(self.imagem_exp)
            self.imagem_atual = self.imagem_exp
            self.redimensionar_imagem(self.imagem_exp)
        else:
            # Janela que avisa que não tem imagem
            self.aviso()

    

    def aplicar_aumento(self):
        if self.imagem_original is not None:
            self.imagem_zoom = cv2.resize(self.imagem_original, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            self.imagem_atual = self.imagem_zoom
            self.redimensionar_imagem(self.imagem_zoom)
        else:
            self.aviso()



    def aplicar_diminuicao(self):
        if self.imagem_original is not None:
            self.imagem_zoom = cv2.resize(self.imagem_original, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
            self.imagem_atual = self.imagem_zoom
            self.redimensionar_imagem(self.imagem_atual)

        else:
            self.aviso()

    
    def brilho(self, opcao):
        if self.imagem_original is not None:
            if opcao == '+':
                self.intensidade_brilho += 0.5
            elif opcao == '-':
                self.intensidade_brilho -= 0.5
            self.aplicar_brilho()

        else:
            self.aviso()      

    def aumentar_brilho(self):
        self.brilho('+')

    def diminuir_brilho(self):
        self.brilho('-')

    def aplicar_brilho(self):
        if self.imagem_original is not None:
            self.imagem_brilho = cv2.convertScaleAbs(self.imagem_original, beta=self.intensidade_brilho * 10)
            self.imagem_atual = self.imagem_brilho
            self.redimensionar_imagem(self.imagem_brilho)
        else:
            self.aviso()

    def contraste(self, opcao):
        if self.imagem_original is not None:
            if opcao == '+':
                self.intensidade_contraste += 0.2
            elif opcao == '-':
                self.intensidade_contraste -= 0.2
            self.aplicar_contraste()

        else:
            self.aviso()     

    def aumentar_contraste(self):
        self.contraste('+')

    def diminuir_contraste(self):
        self.contraste('-')

    def aplicar_contraste(self):
        if self.imagem_original is not None:
            imagem_contraste = cv2.convertScaleAbs(self.imagem_original, alpha=self.intensidade_contraste)
            self.imagem_atual = imagem_contraste
            self.redimensionar_imagem(imagem_contraste)
        else:
            self.aviso()
    
    def histograma(self):
        if self.imagem_original is not None:
            self.exibir_hist(self.imagem_original)
        else:
            self.aviso()

    def exibir_hist(self, imagem):
        if imagem is not None:
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


    def histograma_equalizado(self):
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

        else:
            self.aviso()

    def histograma_especificacao(self):
        caminho_referencia = filedialog.askopenfilename()

        if caminho_referencia is not None:
            img_entrada = self.imagem_original
            img_referencia = cv2.imread(caminho_referencia)

            # calcula os histogramas normalizados
            pr = [cv2.calcHist([chan], [0], None, [256], [0, 256]).ravel() for chan in cv2.split(img_entrada)]
            pz = [cv2.calcHist([chan], [0], None, [256], [0, 256]).ravel() for chan in cv2.split(img_referencia)]
            # calcula os histogramas acumulados
            cdf_input = [np.cumsum(hist) for hist in pr]
            cdf_ref = [np.cumsum(hist) for hist in pz]

            img_out = np.zeros(img_entrada.shape, dtype=np.uint8)

            for c in range(3):
                for i in range(256):
                    diff = np.absolute(cdf_ref[c] - cdf_input[c][i])
                    indice = diff.argmin()
                    img_out[img_entrada[:, :, c] == i, c] = indice
            
            self.imagem_atual = img_out
            self.redimensionar_imagem(img_out)

        
    def filtro_box(self):
        if self.imagem_original is not None:
            kernel = int(self.input_box.get())
            self.imagem_box = cv2.blur(self.imagem_original, (kernel, kernel), borderType=0) # (5,5) = tamanho do kernel
            self.imagem_atual = self.imagem_box
            self.redimensionar_imagem(self.imagem_box)
        
        else:
            self.aviso()
    
    def filtro_gaussiano(self):
        if self.imagem_original is not None:
            kernel = int(self.input_gaussiano.get())
            # GaussianBlur tem 3 parâmetros:
            # 1 - Imagem de entrada
            # 2 - Tamanho do kernel
            # 3 - Desvio padrão em X e Y 
            # Conta do desvio padrão: kernel 
            if kernel % 2 != 0:
                sigma = round((kernel - 1) / 6.0)
                print(sigma)
                self.imagem_gauss = cv2.GaussianBlur(self.imagem_original, (kernel, kernel), sigmaX=sigma, borderType=0) 
                self.imagem_atual = self.imagem_gauss
                self.redimensionar_imagem(self.imagem_gauss)
        
        else:
            self.aviso()

    def filtro_mediana(self):
        if self.imagem_original is not None:
            kernel = int(self.input_mediana.get())
            if kernel % 2 != 0:
                self.imagem_mediana = cv2.medianBlur(self.imagem_original, kernel)
                self.imagem_atual = self.imagem_mediana
                self.redimensionar_imagem(self.imagem_mediana)

        else:
            self.aviso()

    def filtro_laplaciano(self):
        if self.imagem_original is not None:
            kernel = int(self.input_laplaciano.get())
            if kernel % 2 != 0:
                # Passo 1: Suavizar a imagem com o filtro gaussiano
                imagem_suavizada = cv2.GaussianBlur(self.imagem_original, (kernel, kernel), 0, 0)


                # Passo 2: Calcular a Laplaciana da imagem suavizada
                laplaciana = cv2.Laplacian(imagem_suavizada, cv2.CV_8U, ksize=5)
                laplaciana = cv2.cvtColor(laplaciana, cv2.COLOR_BGR2GRAY)
                
                self.imagem_original = laplaciana
                self.redimensionar_imagem(laplaciana)
        
        else:
            self.aviso()

    def filtro_sobel(self):
        if self.imagem_original is not None:
            kernel = int(self.input_sobel.get())
            if kernel % 2 != 0:

                # Carrega a imagem suavizada
                imagem_suavizada = cv2.GaussianBlur(self.imagem_original, (kernel, kernel), 0, 0)

                sobel = cv2.Sobel(imagem_suavizada, cv2.CV_8U, 1, 1, ksize=5)
                sobel = cv2.cvtColor(sobel, cv2.COLOR_BGR2GRAY)
                self.redimensionar_imagem(sobel)

        else:
            self.aviso()



    def filtro_canny(self):
        if self.imagem_original is not None:
            imagem_original = cv2.cvtColor(self.imagem_original, cv2.COLOR_BGR2GRAY)
            imagem_gaussiana = cv2.GaussianBlur(imagem_original, (1, 1), 1)

             # Canny tem 5 parametros:
            # 1 - Imagem de entrada
            # 2 - Limite inferior
            # 3 - Limite superior
            # 4 - Tamanho do kernel
            # 5 - Se True, usa a fórmula L2 para calcular a magnitude do gradiente. Se False, usa a fórmula L1 que é a soma dos valores absolutos das derivadas em x e y 
            bordas = cv2.Canny(imagem_gaussiana, 100, 200, 3, L2gradient=False)

            self.imagem_atual = bordas

            self.redimensionar_imagem(bordas)

    def filtro_limiarizacao(self):
        if self.imagem_original is not None:
            imagem_original = cv2.cvtColor(self.imagem_original, cv2.COLOR_BGR2RGB)

            imagem_cinza = cv2.cvtColor(imagem_original, cv2.COLOR_BGR2GRAY)

            # Limiarização simples
            # Se o valor do pixel for maior que 127, ele vai ser branco (255)
            # Se o valor do pixel for menor que 127, ele vai ser preto (0)
            _, imagem_limiarizada = cv2.threshold(imagem_cinza, 127, 255, cv2.THRESH_BINARY)

            self.imagem_atual = imagem_limiarizada

            self.redimensionar_imagem(imagem_limiarizada)

        else:
            self.aviso()


    def filtro_hough(self):
        if self.imagem_original is not None:
            self.imagem_original = cv2.cvtColor(self.imagem_original, cv2.COLOR_BGR2RGB)

            imagem_cinza = cv2.cvtColor(self.imagem_original, cv2.COLOR_BGR2GRAY)

            imagem_suavizada = cv2.GaussianBlur(imagem_cinza, (5, 5), 0)

            bordas = cv2.Canny(imagem_suavizada, 100, 200, apertureSize=3, L2gradient=True)

            # A função HoughLines tem 7 parâmetros:
            # 1 - Imagem de entrada
            # 2 - Resolução do parâmetro ro do espaço de Hough
            # 3 - Resolução do parâmetro teta do espaço de Hough
            # 4 - Limiar para a contagem de votos
            # 5 - Vetor de saída de linhas. Cada linha é representada por um vetor de 2 elementos (ro e teta)
            # 6 - A resolução do parâmetro ro do espaço de Hough em relação à resolução da imagem
            # 7 - A resolução do parâmetro teta do espaço de Hough em relação à resolução da imagem

            lines = cv2.HoughLines(bordas, 1, np.pi / 180, 150, None, 0, 0)
            ## [hough_lines]
            ## [draw_lines]
            # Draw the lines
            if lines is not None:
                for i in range(0, len(lines)):
                    rho = lines[i][0][0]
                    theta = lines[i][0][1]
                    a = math.cos(theta)
                    b = math.sin(theta)
                    x0 = a * rho
                    y0 = b * rho
                    pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
                    pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))

                    # line() é uma função do OpenCV que desenha uma linha entre dois pontos
                    # Ela recebe como parâmetros:
                    # 1 - Imagem de entrada
                    # 2 - Ponto inicial
                    # 3 - Ponto final
                    # 4 - Cor da linha
                    # 5 - Espessura da linha
                    # 6 - Tipo da linha
                    cv2.line(self.imagem_original, pt1, pt2, (0,255,0), 3, cv2.LINE_AA)
            
                self.imagem_atual = self.imagem_original
                self.redimensionar_imagem(self.imagem_original)

            else:
                print("Nenhuma linha encontrada")
        else: 
            self.aviso()




if __name__ == "__main__":
    root = tk.Tk() # root 
    app = EditorImagem(root) 
    root.mainloop()
