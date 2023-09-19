from flask import (Flask, render_template, 
                   request, redirect, 
                   url_for, flash)
import io
from bson.binary import Binary

from db import categorias, preguntas, examenes
from validaciones import (validar_crear_categoria, 
                          validar_editar_categoria, 
                          validar_eliminar_categoria, 
                          validar_crear_pregunta)

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'pBsMG9T=Vjz*yDb}64$twh'

@app.route('/')
def iniciar():
    texto = 'Una pequeña prueba'
    return render_template('/inicio/index.html', texto=texto)

@app.route('/preguntas', methods=['GET', 'POST'])
def listar_preguntas():
    previos = categorias.count_documents({'estatus': 'A'})
    revisado = True
    if previos == 0: 
        revisado = False
        return render_template('/preguntas/listar/index.html', 
                               revisado=revisado)
    divisiones = categorias.find({'estatus': 'A'})
    lista = preguntas.find({'estatus': 'A'})
    if request.method == 'POST': 
        forma = request.form
        tipo = forma['categoria']
        lista = preguntas.find({'categoria': tipo, 'estatus': 'A'})

    return render_template('/preguntas/listar/index.html', 
                           revisado=revisado, 
                           lista=lista, 
                           divisiones=divisiones)

@app.route('/pregunta', methods=['GET', 'POST'])
def crear_pregunta():
    divisiones = categorias.find({'estatus': 'A'})
    if request.method == 'POST':
        forma = request.form
        numero = preguntas.count_documents({}) + 1
        nueva_pregunta = {
            'id': 'E' + str(numero), 
            'nombre': str(forma['nombre']), 
            'categoria': forma['categoria'], 
            'puntaje': forma['puntaje'], 
            'tipo': forma['tipo'], 
            'imagen': forma['imagen'], 
            'estatus': 'A'
        }
        if forma['tipo'] == 'seleccion': 
            nueva_pregunta['respuestas'] = forma['respuestas']
        if validar_crear_pregunta(nueva_pregunta):
            nueva_pregunta['precio'] = int(forma['precio'])
            id = preguntas.insert_one(nueva_pregunta).inserted_id
            if id:
                flash('Pregunta creada con éxito')
                return redirect(url_for('listar_preguntas'))
            else: 
                flash('Ocurrió un error guardando')
        else: flash('La pregunta no pasó las validaciones')
    return render_template('/preguntas/crear/index.html', 
                           divisiones=divisiones)

@app.route('/pregunta/<id>', methods=['GET'])
def consultar_pregunta(id):
    return render_template('/preguntas/crear/index.html')

@app.route('/pregunta/<id>/modificar', methods=['GET', 'POST'])
def modificar_pregunta(id):
    return render_template('/preguntas/modificar/index.html')

@app.route('/pregunta/<id>/eliminar', methods=['GET', 'POST'])
def eliminar_pregunta(id):
    return render_template('/preguntas/modificar/index.html')

@app.route('/categorias', methods=['GET'])
def listar_categorias():
    lista = categorias.find({'estatus': 'A'})
    prueba = []
    for esto in categorias.find({'estatus': 'A'}):
        nueva = {
            'id': esto['id'], 
            'nombre': esto['nombre'], 
            'descripcion': esto['descripcion']
        }
        prueba.append(nueva)
    return render_template('/categorias/listar/index.html', 
                           lista=lista, 
                           prueba=prueba)

@app.route('/categoria', methods=['GET', 'POST'])
def crear_categoria():
    if request.method == 'POST':
        numero = categorias.count_documents({}) + 1
        forma = request.form
        nueva_categoria = {
            'id': 'C' + str(numero), 
            'nombre': forma['nombre'], 
            'descripcion': forma['descripcion'], 
            'estatus': 'A'
        }
        if validar_crear_categoria(nueva_categoria):
            id = categorias.insert_one(nueva_categoria).inserted_id
            if id:
                flash('Categoría creada con éxito')
                return redirect(url_for('listar_categorias'))
            else: 
                flash('Ocurrió un error guardando')
        else: flash('Se ingresó un nombre repetido')
    return render_template('/categorias/crear/index.html')

@app.route('/categoria/<id>', methods=['GET'])
def consultar_categoria(id):
    categoria = categorias.find_one({'id': id, 'estatus': 'A'})
    return render_template('/categorias/consultar/index.html', 
                           categoria=categoria)

@app.route('/categoria/<id>/modificar', methods=['GET', 'POST'])
def modificar_categoria(id):
    vieja = categorias.find_one({'id': id, 'estatus': 'A'})

    if not vieja:
        flash('Categoría no encontrada')
        return redirect(url_for('listar_categorias'))
    
    if request.method == 'POST':
        forma = request.form
        nueva_categoria = {
            'nombre': forma['nombre'], 
            'descripcion': forma['descripcion'], 
        }
        if validar_editar_categoria(nueva_categoria):
            busqueda = {'id': id, 'estatus': 'A'}
            final = {'$set': nueva_categoria}
            categorias.update_one(busqueda, final)
            return redirect(url_for('listar_categorias'))
        else: flash('Se ingresó un nombre repetido')
    return render_template('/categorias/modificar/index.html', 
                           vieja_categoria=vieja)

@app.route('/categoria/<id>/eliminar', methods=['GET', 'POST'])
def eliminar_categoria(id):
    vieja = categorias.find_one({'id': id, 'estatus': 'A'})

    if not vieja:
        flash('Categoría no encontrada')
        return redirect(url_for('listar_categorias'))
    
    if request.method == 'POST':
        if validar_eliminar_categoria(vieja):
            busqueda = {'id': id, 'estatus': 'A'}
            final = {'$set': {'estatus': 'I'}}
            categorias.update_one(busqueda, final)
            flash('Categoría eliminada con éxito')
            return redirect(url_for('listar_categorias'))
        else: flash('No se puede eliminar categorías que están en uso')
    return render_template('/categorias/eliminar/index.html', 
                           vieja_categoria=vieja)

@app.route('/examenes')
def listar_examenes(): 
    return render_template('/examenes/index.html')

@app.route('/examen', methods=['GET', 'POST'])
def crear_examen():
    return render_template('/examenes/crear/index.html')

@app.route('/examen/<id>', methods=['GET'])
def consultar_examen(id):
    return render_template('/examenes/crear/index.html')

@app.route('/examen/<id>', methods=['GET', 'POST'])
def modificar_examen(id):
    return render_template('/examenes/modificar/index.html')

@app.route('/examen/<id>', methods=['GET', 'POST'])
def eliminar_examene(id):
    return render_template('/examenes/modificar/index.html')

if __name__ == '__main__':
    app.run(debug=True)