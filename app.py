from flask import Flask, render_template, request, redirect, url_for, flash
import io
from db import categorias, notas, examenes
from validaciones import validar_crear_categoria

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'pBsMG9T=Vjz*yDb}64$twh'

@app.route('/')
def iniciar():
    texto = 'Una pequeña prueba'
    return render_template('/inicio/index.html', texto=texto)

@app.route('/preguntas', methods=['GET'])
def listar_preguntas():
    return render_template('/preguntas/listar/index.html')

@app.route('/pregunta', methods=['GET', 'POST'])
def crear_preguntas():
    return render_template('/preguntas/crear/index.html')

@app.route('/pregunta/<id>', methods=['GET'])
def consultar_pregunta(id):
    return render_template('/preguntas/crear/index.html')

@app.route('/pregunta/<id>', methods=['GET', 'POST'])
def modificar_pregunta(id):
    return render_template('/preguntas/modificar/index.html')

@app.route('/pregunta/<id>', methods=['GET', 'POST'])
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

@app.route('/categoria/<id>/modificar', methods=['GET', 'PUT'])
def modificar_categoria(id):
    
    return render_template('/categorias/modificar/index.html')

@app.route('/categoria/<id>/eliminar', methods=['GET', 'DELETE'])
def eliminar_categoria(id):
    return render_template('/categorias/eliminar/index.html')

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