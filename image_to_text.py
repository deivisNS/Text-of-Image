from PIL import Image, ImageEnhance	#abrir y cambiar el contraste
import pytesseract	#para sacar texto de imagenes
import os 





class Buscar_Text():


	pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"	#definir la ruta del ejecutable


	strings = []



	def __init__(self, ruta_imagen, resize = 0):


		self.imagen = Image.open(ruta_imagen)	#abrimos la imagen
		
		width, height = self.imagen.size 	#tomamos lo ancho y largo de la imagen


		if resize != 0:
			
			self.imagen = self.imagen.resize((width * resize, height * resize))	#redimensiona la imagen (aumenta)  

			mejorar = ImageEnhance.Contrast(self.imagen)	#modulo para el contraste de las imagenes

			self.imagen = mejorar.enhance(2.1)	#mejoramos el contraste 1.0 > es el estandar

			width, height = self.imagen.size


		self.boxes_2_parts = [	#caja de dimensiones para recortar la imagen
			(0, 0, width, height // 2),
			(0, height // 2, width, height)
			]
				
		self.boxes_4_parts = [	#caja de dimensiones para recortar la imagen
			(0, 0, width // 2, height // 2),
			(width // 2, 0, width, height // 2),

			(0, height // 2, width // 2, height),
			(width // 2, height // 2, width, height)
			]

		self.boxes_9_parts = [	#caja de dimensiones para recortar la imagen
			(0, 0, width // 3, height // 3),
			(width // 3, 0, (width // 3) * 2, height // 3),
			((width // 3) * 2, 0, width, height // 3),

			(0, height // 3, width // 3, (height // 3) * 2),
			(width // 3, height // 3, (width // 3) * 2, (height // 3) * 2),
			((width // 3) * 2, height // 3, width, (height // 3) * 2),

			(0, (height // 3) * 2, width // 3, height),
			(width // 3, (height // 3) * 2, (width // 3) * 2, height),
			((width // 3) * 2, (height // 3) * 2, width, height),
			]

		self.from_3_column = [	#caja de dimensiones para recortar la imagen
			(0, 0, width // 3, height),
			(width // 3, 0, (width // 3) * 2, height),
			((width // 3) * 2, 0, width, height)
			]

		self.from_3_row = [	#caja de dimensiones para recortar la imagen
			(0, 0, width, height // 3),
			(0, height // 3, width, (height // 3) * 2),
			(0, (height // 3) * 2, width, height)
			]



	#busca texto en dos partes de la imagen
	def from_2_parts(self, with_cut = False):
		

		self.strings = []


		for box in self.boxes_2_parts:
			
			if with_cut == False:
				
				self.process(box)


			else:
				
				self.processing_cuts(box)
						
		
		if with_cut == False:
	
			return self.strings


		else:

			return self.text_to_cuts()



	#busca texto en cuatro partes de la imagen
	def from_4_parts(self, with_cut = False):
		

		self.strings = []


		for box in self.boxes_4_parts:
			
			if with_cut == False:
				
				self.process(box)


			else:
				
				self.processing_cuts(box)
						
		
		if with_cut == False:
	
			return self.strings


		else:

			return self.text_to_cuts()



	#busca texto en nueve partes de la imagen
	def from_9_parts(self, with_cut = False):
		

		self.strings = []


		for box in self.boxes_9_parts:
	
			if with_cut == False:
				
				self.process(box)


			else:
				
				self.processing_cuts(box)
						
		
		if with_cut == False:
	
			return self.strings


		else:

			return self.text_to_cuts()



	#busca tetxo en tres partes de la imagen en forma de columnas
	def from_3_column_parts(self, with_cut = False):
		

		self.strings = []


		for box in self.from_3_column:
	
			if with_cut == False:
				
				self.process(box)


			else:
				
				self.processing_cuts(box)
						
		
		if with_cut == False:
	
			return self.strings


		else:

			return self.text_to_cuts()



	#busca texto en tres partes de la imagen en forma de filas		
	def from_3_row_parts(self, with_cut = False):
		

		self.strings = []


		for box in self.from_3_row:
	
			if with_cut == False:
				
				self.process(box)


			else:
				
				self.processing_cuts(box)
						
		
		if with_cut == False:
	
			return self.strings


		else:

			return self.text_to_cuts()



	def processing_cuts(self, box):
		

		if os.path.exists("Cortes") == False:

			os.mkdir("Cortes")


		part = self.imagen.crop(box)	#cortamos la imagen

		part.save(f"Cortes/{box}.png")	#guardamos el corte



	#extrae el texto y guarda cortes de la imagen 
	def text_to_cuts(self):
		

		cortes = os.listdir("Cortes")


		for C in cortes:

			img = Image.open(f"Cortes/{C}")

			#print(pytesseract.image_to_osd(img))	

			
			clean_string = pytesseract.image_to_string(
				img, 
				lang = "spa"
				#config = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
				)

			clean_string = clean_string.replace("\n", " ")

			clean_string = clean_string.replace("  ", " ")

			clean_string = clean_string.replace("- ", "-") 


			if clean_string:
	
				self.strings.append(clean_string)


		return self.strings			



	def process(self, box):


		func = lambda x: x * 0.5 if x > 50 else x 	#funcion lambda para que los colores de la imagen disminuyan a exepcion del color negro

		part = self.imagen.crop(box)	#cortamos parte de la imagen
		
		part = part.point(func)	#disminuimos los demas colores, menos el negro

		clean_string = pytesseract.image_to_string(  #imprimimos el texto sacado
			part, 
			lang = "eng"
			#config = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
			)

		clean_string = clean_string.replace("\n", " ")

		clean_string = clean_string.replace("  ", " ")

		clean_string = clean_string.replace("- ", "-") 

		clean_string = clean_string.replace("/", "")

		clean_string = clean_string.replace("{", "")
		
		clean_string = clean_string.replace("}", "")

		clean_string = clean_string.replace("|", "")

		if clean_string:	
	
			self.strings.append(clean_string)




"""si en ocasiones al extraer el texto aparecen simbolos, letras que no estaban o no extrae alguna parte,
es debido porque la imagen no es muy legible o ya a pasado por varias traducciones"""

a = Buscar_Text("imagen 2.jpg", resize = 4)	#rezise es para agrandar la imagen y aumentar el contraste

print(a.from_4_parts())	#el with_cut es para que extraiga y guarde cortes de la imagen

#b = Buscar_Text("imagen.jpg", resize = 3)

#print(b.from_2_parts())

