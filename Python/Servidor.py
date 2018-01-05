__author__ = "201403610 - 201443726"

from flask import Flask, request, Response
import subprocess, Matriz, ArbolB, ArbolBinario, ListaCanciones, ListaDoble

app = Flask("ProyectoDic2017")

# ESTRUCTURAS
repertorio = Matriz.Matriz() # Todo
artistas = ArbolB.ArbolB(5) # auxiliar
albumes = ArbolBinario.ArbolBinario() # auxiliar
canciones = ListaCanciones.ListaCanciones() # auxiliar
usuarios = ListaDoble.ListaDoble() # Usuarios

# USUARIO EN EL SISTEMA
logueado = ListaDoble.Usuario("", "")

# RAIZ
@app.route('/', methods = ['GET'])
def init():
	return "metodos: /ingresar, /salir, /insertar_usuario, /agregar_cancion, /eliminar_ano, /eliminar_genero, /eliminar_artistas, /eliminar_artista, /eliminar_album, eliminar_cancion..."

# LOGIN
@app.route('/ingresar', methods = ['POST'])
def ingresar():
	nombre = (request.form['nombre']).encode('ISO-8859-1')
	contrasena = (request.form['contrasena']).encode('ISO-8859-1')
	lg = usuarios.buscar(nombre, contrasena)
	if lg == None:
		return "Credenciales incorrectas."
	logueado = lg.Usuario
	return "Ingreso exitoso."

# LOGOUT
@app.route('/salir', methods = ['POST'])
def salir():
	txt = str(request.form['txt'])
	logueado = ListaDoble.Usuario("", "")
	return ""

# INSERTAR
@app.route('/insertar_usuario', methods = ['POST'])
def insertar_usuario():
	nombre = (request.form['nombre']).encode('ISO-8859-1')
	contrasena = (request.form['contrasena']).encode('ISO-8859-1')
	if usuarios.insertar(nombre, contrasena):
		return "Usuario creado."
	return "Nombre de usuario ya en uso."

@app.route('/agregar_a_lista', methods = ['POST'])
def agregar_a_lista():
	nombre = (request.form['nombre']).encode('ISO-8859-1')
	path = (request.form['path']).encode('ISO-8859-1')
	if logueado.nombre != "":
		if logueado.lista != None:
			logueado.lista.insertar(nombre, path)
		else:
			logueado.lista = ListaCanciones.ListaCanciones()
			logueado.lista.insertar(nombre, path)
	return ""	

@app.route('/agregar_cancion', methods=['POST'])
def agregar_cancion():
	ano = (request.form['ano']).encode('ISO-8859-1')
	genero = (request.form['genero']).encode('ISO-8859-1')
	artista = (request.form['artista']).encode('ISO-8859-1')
	album = (request.form['album']).encode('ISO-8859-1')
	nombre = (request.form['nombre']).encode('ISO-8859-1')
	path = (request.form['path']).encode('ISO-8859-1')
	ab = repertorio.obtenerArtistas(ano, genero)
	if (ab == None): # No existe el nodo con ese ano y genero: se inserta desde la matriz
		canciones = ListaCanciones.ListaCanciones()
		canciones.insertar(nombre, path)
		albumes = ArbolBinario.ArbolBinario()
		albumes.insertar(album, canciones)
		artistas = ArbolB.ArbolB(5)
		artistas.insertar(artista, albumes)
		repertorio.insertar(ano, genero, artistas)
	else: # Si existe el nodo con ese ano y genero
		indice = 0
		pagina = None
		pagina, indice = ab.artistas.buscar(ab.artistas.raiz, artista, indice)
		if pagina == None: # No existe el nodo con ese artista: se inserta desde el arbol b
			canciones = ListaCanciones.ListaCanciones()
			canciones.insertar(nombre, path)
			albumes = ArbolBinario.ArbolBinario()
			albumes.insertar(album, canciones)
			ab.artistas.insertar(artista, albumes)
		else: # Si existe el nodo con ese artista
			abb = pagina.nodos[indice].albumes
			lc = abb.buscar(album)
			if lc == None: # No existe el nodo con ese album: se inserta desde el arbol binario de busqueda
				canciones = ListaCanciones.ListaCanciones()
				canciones.insertar(nombre, path)
				abb.insertar(album, canciones)
			else: # Si existe el nodo con ese album: se inserta solo en la lista de canciones
				lc.lista.insertar(nombre, path)
	return ""

# ELIMINAR
@app.route('/eliminar_usuario', methods=['POST'])
def eliminar_usuario():
	nombre = (request.form['nombre']).encode('ISO-8859-1')
	contrasena = (request.form['contrasena']).encode('ISO-8859-1')
	usuario_ = usuarios.buscar(nombre, contrasena)
	if usuario_ != None:
		usuarios.eliminar(nombre)
	return ""

@app.route('/eliminar_ano', methods=['POST'])
def eliminar_ano():
	ano = (request.form['ano']).encode('ISO-8859-1')
	auxiliar = repertorio.inicio.derecha
	while auxiliar != None:
		repertorio.eliminar(ano, auxiliar.genero)
		auxiliar = auxiliar.derecha
	return ""

@app.route('/eliminar_genero', methods=['POST'])
def eliminar_genero():
	genero = (request.form['genero']).encode('ISO-8859-1')
	auxiliar = repertorio.inicio.abajo
	while auxiliar != None:
		repertorio.eliminar(auxiliar.ano, genero)
		auxiliar = auxiliar.abajo
	return ""

@app.route('/eliminar_artistas', methods=['POST'])
def eliminar_artistas():
	ano = (request.form['ano']).encode('ISO-8859-1')
	genero = (request.form['genero']).encode('ISO-8859-1')
	repertorio.eliminar(ano, genero)
	return ""

@app.route('/eliminar_artista', methods=['POST'])
def eliminar_artista():
	artista = (request.form['artista']).encode('ISO-8859-1')
	if repertorio.id != 1:
		nodoFila = repertorio.inicio.abajo
		nodoDato = None
		while nodoFila != None:
			nodoDato = nodoFila.derecha
			while nodoDato != None:
				nodoDato.artistas.eliminar(artista)
				if nodoDato.artistas.raiz.cuenta == 0:
					repertorio.eliminar(nodoDato.ano, nodoDato.genero)
				nodoDato = nodoDato.derecha
			nodoFila = nodoFila.abajo
	return ""

@app.route('/eliminar_album', methods=['POST'])
def eliminar_album():
	ano = (request.form['ano']).encode('ISO-8859-1')
	genero = (request.form['genero']).encode('ISO-8859-1')
	artista = (request.form['artista']).encode('ISO-8859-1')
	album = (request.form['album']).encode('ISO-8859-1')
	ab = repertorio.obtenerArtistas(ano, genero)
	if ab != None:
		indice = 0
		pagina = None
		pagina, indice = ab.artistas.buscar(ab.raiz, artista, bandera)
		if pagina != None:
			abb = pagina.nodos[indice].albumes
			abb.eliminar(album)
			if abb.nodo == None:
				ab.artistas.eliminar(artista)
				if ab.artistas.raiz.cuenta == 0:
					repertorio.eliminar(ano, genero)
	return ""

@app.route('/eliminar_cancion', methods=['POST'])
def eliminar_cancion():
	ano = (request.form['ano']).encode('ISO-8859-1')
	genero = (request.form['genero']).encode('ISO-8859-1')
	artista = (request.form['artista']).encode('ISO-8859-1')
	album = (request.form['album']).encode('ISO-8859-1')
	nombre = (request.form['nombre']).encode('ISO-8859-1')
	ab = repertorio.obtenerArtistas(ano, genero)
	if ab != None:
		indice = 0
		pagina = None
		pagina, indice = ab.artistas.buscar(ab.raiz, artista, bandera)
		if pagina != None:
			abb = pagina.nodos[indice].albumes
			lc = abb.buscar(album)
			if lc != None:
				lc.lista.eliminar(nombre)
				if lc.lista.inicio == None:
					abb.eliminar(album)
					if abb.nodo == None:
						ab.artistas.eliminar(artista)
						if ab.artistas.raiz.cuenta == 0:
							repertorio.eliminar(ano, genero)
	return ""

# GRAFICAR
@app.route('/graficar_matriz', methods=['POST'])
def graficar_matriz():
	txt = str(request.form['txt'])
	repertorio.graficar()
	return ""

@app.route('/graficar_arbol_b', methods=['POST'])
def graficar_arbol_b():
	ano = (request.form['ano']).encode('ISO-8859-1')
	genero = (request.form['genero']).encode('ISO-8859-1')
	ab = repertorio.obtenerArtistas(ano, genero)
	if ab != None:
		ab.artistas.graficar()
	return ""

@app.route('/graficar_abb', methods=['POST'])
def graficar_abb():
	ano = (request.form['ano']).encode('ISO-8859-1')
	genero = (request.form['genero']).encode('ISO-8859-1')
	artista = (request.form['artista']).encode('ISO-8859-1')
	ab = repertorio.obtenerArtistas(ano, genero)
	if ab != None:
		indice = 0
		pagina = None
		pagina, indice = ab.artistas.buscar(ab.artistas.raiz, artista, indice)
		if pagina != None:
			pagina.nodos[indice].albumes.graficar()
	return ""

@app.route('/graficar_lista_circular', methods=['POST'])
def graficar_lista_circular():
	ano = (request.form['ano']).encode('ISO-8859-1')
	genero = (request.form['genero']).encode('ISO-8859-1')
	artista = (request.form['artista']).encode('ISO-8859-1')
	album = (request.form['album']).encode('ISO-8859-1')
	ab = repertorio.obtenerArtistas(ano, genero)
	if ab != None:
		indice = 0
		pagina = None
		pagina, indice = ab.artistas.buscar(ab.artistas.raiz, artista, indice)
		if pagina != None:
			abb = pagina.nodos[indice].albumes
			lc = abb.buscar(album)
			if lc != None:
				lc.lista.graficar()
	return ""

@app.route('/graficar_lista_doble', methods=['POST'])
def graficar_lista_doble():
	txt = str(request.form['txt'])
	usuarios.graficar()
	return ""

@app.route('/graficar_lista_circular_usuario', methods=['POST'])
def graficar_lista_circular_usuario():
	txt = str(request.form['txt'])
	if logueado.nombre != "":
		if logueado.lista != None:
			logueado.lista.graficar()
	return ""

# OBTENER - REPRODUCIR
#@app.route('', methods = ['POST'])

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')