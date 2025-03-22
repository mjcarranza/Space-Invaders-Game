import sys
import time
import tkinter as tk
class AnimatedGif(tk.Label):
	"""
	Clase que muestra el archivo gif Animado en una etiqueta
	Se usa el metodo start() para empezar la animacion
	"""
	def __init__(self, root, gif_file, delay=0.04):
		"""
		:param gif_file: nombre del archivo del gif
		:param delay: duracion de descanso entre cada animacion
		"""
		tk.Label.__init__(self, root, bg = "black")
		self.root = root
		self.gif_file = gif_file
		self.delay = delay
		self.stop = False  # para parar el hilo

		self._num = 0

	def start(self):
		"""Inicia un hilo para manejarlo manualmente"""
		self.start_time = time.time()  # Empezamos un timer
		self._animate()

	def stop(self):
		""" para la animacion """
		self.stop = True

	def _animate(self):
		try:
			self.gif = tk.PhotoImage(file=self.gif_file, format='gif -index {}'.format(self._num))  # Iniciamos el gif
			self.configure(image=self.gif)
			self._num += 1
		except tk.TclError:  
			self._num = 0
		if not self.stop:    # Si paramos ya no se repite
			self.root.after(int(self.delay*1000), self._animate)

	def start_thread(self):
		""" Empieza el hilo """
		from threading import Thread  # importamos el modulo si lo necesitamos
		self._animation_thread = Thread()
		self._animation_thread = Thread(target=self._animate_thread).start()  # Empezamos el hilo automatico

	def stop_thread(self):
		""" Paramos el hilo de la animacion """
		self.stop = True

	def _animate_thread(self):
		""" Actualizamos la animacion si esta corriendo en otro hilo """
		while self.stop is False:
			try:
				time.sleep(self.delay)
				self.gif = tk.PhotoImage(file=self.gif_file, format='gif -index {}'.format(self._num))
				self.configure(image=self.gif)
				self._num += 1
			except tk.TclError:
				self._num = 0
			except RuntimeError:
				sys.exit()
