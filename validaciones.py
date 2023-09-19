from db import categorias, examenes, preguntas

def validar_crear_categoria(categoria):
    verdad = True
    lista = categorias.find({'estatus': 'A'})
    for esto in lista: 
        if (categoria['nombre'] == esto['nombre'] or 
            categoria['id'] == esto['id']): 
            verdad = False
            break
    return verdad

def validar_editar_categoria(categoria): 
    verdad = True
    lista = categorias.find({'estatus': 'A'})
    for esto in lista:
        if (categoria['nombre'] == esto['nombre'] and 
            categoria['id'] != esto['id']): 
            verdad = False
            break
    return verdad

def validar_eliminar_categoria(categoria):
    verdad = True
    lista = preguntas.find({'estatus': 'A'})
    for esto in lista: 
        if categoria['id'] == esto['categoria']: 
            verdad = False
            break
    return verdad

def validar_crear_pregunta(pregunta): 
    verdad = True
    return verdad