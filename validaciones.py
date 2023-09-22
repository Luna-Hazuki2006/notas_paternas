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
    lista = preguntas.find({'estatus': 'A'})
    for esto in lista: 
        if (pregunta['nombre'] == esto['nombre'] or 
            pregunta['id'] == esto['id']): 
            verdad = False
            break
    return verdad

def validar_editar_pregunta(pregunta):
    verdad = True
    lista = preguntas.find({'estatus': 'A'})
    for esto in lista:
        if (pregunta['nombre'] == esto['nombre'] and 
            pregunta['id'] != esto['id']): 
            verdad = False
            break
    return verdad

def validar_eliminar_pregunta(pregunta):
    verdad = True
    lista = examenes.find({'estatus': 'A'})
    for esto in lista['hojas']:
        for esta in esto['secciones']: 
            for aquella in esta['preguntas']: 
                if (pregunta['id'] == aquella):
                    verdad = False
                    break
    return verdad

def validar_crear_examen(examen):
    verdad = True
    lista = examenes.find({'estatus': 'A'})
    for esto in lista: 
        if esto['id'] == examen['id']: 
            verdad = False
            break
    return verdad