from tkinter import *



import tkinter as tk

from PIL import ImageTk,Image

from tkinter import filedialog
import os
import predicao

filename = ""

#Escolher o arquivo
def browseFiles(): 
	filename = filedialog.askopenfilename(initialdir = "/", 
										  title = "Selecione um arquivo", 
										  filetypes = (("Todos os Arquivos", 
														"*.*"), 
													   ("Text files", 
														"*.txt*")))
	if filename is not None:
		resultado = predicao.predict(filename)
	
'''def show_result():
	result_window = Tk()
	result_window.geometry('300x300')
	result = Label(window,
					background = "#fceef5",
					text = result,
					font = "bold",
					width = 10000, height = 2,
					fg = "#ea227b"
					)

	result.configure(font=("Roboto", 40))'''
#Janela																								   
window = Tk() 

window.title('M A M E S') 

window.iconbitmap(os.path.join('src', 'Logo.ico'))

window.geometry("1920x1080")

window.maxsize(980,720)

window.minsize(980,720)


canvas = Canvas(window,width=1920,height=1080)

image = ImageTk.PhotoImage(Image.open(os.path.join('src', 'Plano.png')))

background_label = tk.Label(window, image=image)

background_label.image = image

background_label.place(x=0, y=0, relwidth=1, relheight=1)
   
# Create a File Explorer label 
titulo = Label(window,
					background = "#fceef5",
					text = "M A M E S",
					font = "bold",
					width = 10000, height = 2,
					fg = "#ea227b"
					)

titulo.configure(font=("Roboto", 40))

#Botão classificar


botaoclassificar = Button(window,  
						text="Avaliar",
						command = browseFiles,
						borderwidth=0,
						background = "#ea227b",
						fg="#fceef5"
						)

botaoclassificar.configure(font=("Roboto",22,))


#botao sair

botaosair = Button(window,  
					 text="Sair", 
					 command = exit,
					 borderwidth=0,
					 background= "#ea227b",
					 fg="#fceef5"
					 )

botaosair.configure(font=("Arvo",22,))



#Subtitulo
texto = Label(window,
			  background = "#ea227b",
			  text = "Sua classificação de câncer acessível",
			  fg = "#fceef5",
			  width=10000,
			  )

texto.configure(font=("Courier", 16, "italic"))



titulo.pack()

texto.pack()

botaoclassificar.pack()

botaoclassificar.pack(side = "top")

botaoclassificar.pack(pady=150)

botaosair.pack()



window.mainloop() 