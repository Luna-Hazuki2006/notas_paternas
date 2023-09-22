from flask import (Flask, render_template, 
                   request, redirect, 
                   url_for, flash)
from db import categorias, preguntas, examenes
from validaciones import (validar_crear_categoria, 
                          validar_editar_categoria, 
                          validar_eliminar_categoria, 
                          validar_crear_pregunta, 
                          validar_editar_pregunta, 
                          validar_eliminar_pregunta, 
                          validar_crear_examen)
from datetime import datetime
from pprint import pprint
import random
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
        print(tipo)
        if tipo != '':
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
            'id': 'P' + str(numero), 
            'nombre': str(forma['nombre']), 
            'categoria': forma['categoria'], 
            'puntaje': float(forma['puntaje']), 
            'imagen': forma['vistas'], 
            'estatus': 'A'
        }
        if validar_crear_pregunta(nueva_pregunta):
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
    pregunta = preguntas.find_one({'id': id, 'estatus': 'A'})
    dato = pregunta['categoria']
    categoria = categorias.find_one({'id': dato, 'estatus': 'A'})
    pregunta['categoria'] = categoria['nombre']
    return render_template('/preguntas/consultar/index.html', 
                           pregunta=pregunta)

@app.route('/pregunta/<id>/modificar', methods=['GET', 'POST'])
def modificar_pregunta(id):
    vieja = preguntas.find_one({'id': id, 'estatus': 'A'})
    divisiones = categorias.find({'estatus': 'A'})
    if not vieja:
        flash('Pregunta no encontrada')
        return redirect(url_for('listar_preguntas'))
    if request.method == 'POST':
        forma = request.form
        nueva_pregunta = {
            'id': vieja['id'], 
            'nombre': str(forma['nombre']), 
            'categoria': str(forma['categoria']), 
            'puntaje': float(forma['puntaje']), 
            'imagen': forma['vistas']
        }
        if validar_editar_pregunta(nueva_pregunta):
            busqueda = {'id': id, 'estatus': 'A'}
            final = {'$set': nueva_pregunta}
            examenes.update_one(busqueda, final)
            return redirect(url_for('listar_preguntas'))
        else: flash('No pasó las validaciones')
    return render_template('/preguntas/modificar/index.html', 
                           divisiones=divisiones, 
                           vieja_pregunta=vieja)

@app.route('/pregunta/<id>/eliminar', methods=['GET', 'POST'])
def eliminar_pregunta(id):
    vieja = categorias.find_one({'id': id, 'estatus': 'A'})

    if not vieja:
        flash('Pregunta no encontrada')
        return redirect(url_for('listar_preguntas'))
    
    if request.method == 'POST':
        if validar_eliminar_pregunta(vieja):
            busqueda = {'id': id, 'estatus': 'A'}
            final = {'$set': {'estatus': 'I'}}
            categorias.update_one(busqueda, final)
            flash('Pregunta eliminada con éxito')
            return redirect(url_for('listar_preguntas'))
        else: flash('No se puede eliminar preguntas que están en uso')
    return render_template('/preguntas/eliminar/index.html', 
                           vieja_pregunta=vieja)

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
    lista = examenes.find({'estatus': 'A'})
    prueba = []
    for esto in examenes.find({'estatus': 'A'}):
        nueva = {
            'id': esto['id'], 
            'nombre': esto['nombre'], 
            'puntaje_total': esto['puntaje_total'], 
            'cantidad_hojas': esto['cantidad_hojas'], 
            'fecha_creacion': esto['fecha_creacion']
        }
        prueba.append(nueva)
    return render_template('/examenes/listar/index.html', 
                           lista=lista, 
                           prueba=prueba)

@app.route('/examen', methods=['GET', 'POST'])
def crear_examen():
    lista = []
    for esto in categorias.find({'estatus': 'A'}):
        for esta in preguntas.find({'estatus': 'A'}): 
            if esta['categoria'] == esto['id']: 
                categoria = {
                    'id': esto['id'], 
                    'nombre': esto['nombre'], 
                    'descripcion': esto['descripcion'], 
                    'puntaje': 0
                }
                lista.append(categoria)
                break
    for esto in lista:
        numero = 0
        datos = {'categoria': esto['id'], 'estatus': 'A'}
        for esta in preguntas.find(datos): 
            numero += esta['puntaje']
        esto['puntaje'] = numero
    if request.method == 'POST': 
        forma = request.form
        numero = examenes.count_documents({}) + 1
        examen = {
            'id': 'E' + str(numero), 
            'nombre': forma['nombre'], 
            'descripcion': forma['descripcion'], 
            'fecha_creacion': datetime.now(), 
            'cantidad_hojas': int(forma['hojas']), 
            'puntaje_total': float(forma['puntaje_total']), 
            'categorias': [], 
            'hojas': [], 
            'estatus': 'A'
        }
        muchos = []
        for esto in lista:
            try: 
                if forma[esto['id']] is not None:
                    data = forma[esto['id']]
                    puntaje = forma['puntaje' + esto['id']]
                    categoria = {
                        'categoria': data, 
                        'puntaje': puntaje
                    }
                    muchos.append(categoria)
                else: continue
            except Exception:
                continue
        examen['categorias'] = muchos
        muchos = []
        for i in range(examen['cantidad_hojas']): 
            hoja = {
                'secciones': []
            }
            info = {}
            for esto in lista: 
                data = {'categoria': esto['id'], 'estatus': 'A'}
                variedad = []
                for cada in preguntas.find(data): 
                    una = {
                        'id': cada['id'], 
                        'nombre': cada['nombre'], 
                        'puntaje': cada['puntaje']
                    }
                    variedad.append(una)
                random.shuffle(variedad)
                info = {
                    'categoria': esto['id'], 
                    'preguntas': []
                }
                mas = []
                numero = 0
                for esta in variedad:
                    numero += esta['puntaje']
                    mas.append(esta['id'])
                    if numero >= esto['puntaje']: 
                        break
                info['preguntas'] = mas

            hoja['secciones'].append(info)
            muchos.append(hoja)
        examen['hojas'] = muchos
        print(examen)
        if validar_crear_examen(examen):
            id = examenes.insert_one(examen).inserted_id
            if id:
                flash('Examen creado con éxito')
                return redirect(url_for('listar_examenes'))
            else: 
                flash('Ocurrió un error guardando')
        else: flash('El examen no pasó las validaciones')
    return render_template('/examenes/crear/index.html', 
                           lista=lista)

@app.route('/examen/<id>', methods=['GET'])
def consultar_examen(id):
    data = examenes.find_one({'id': id, 'estatus': 'A'})
    pprint(data)
    for esto in data['hojas']:
        muchos = []
        for esta in esto['secciones']['preguntas']: 
            datos = {'id': esta, 'estatus': 'A'}
            pregunta = preguntas.find_one(datos)
            muchos.append(pregunta)
        esto['secciones']['preguntas'] = muchos
    pprint(data)
    return render_template('/examenes/consultar/index.html', 
                           lista=data)

@app.route('/examen/<id>/<hoja>', methods=['GET'])
def consultar_hoja(id, hoja):
    return render_template('/examenes/consultar_hoja/index.html')

@app.route('/examen/<id>', methods=['GET', 'POST'])
def eliminar_examen(id):
    return render_template('/examenes/modificar/index.html')

if __name__ == '__main__':
    app.run(debug=True)