from db import categorias, examenes, notas

def validar_crear_categoria(categoria):
    verdad = True
    lista = categorias.find({'estatus': 'A'})
    for esto in lista: 
        if (categoria['nombre'] == esto['nombre'] or 
            categoria['id'] == esto['id']): 
            verdad = False
            break
    return verdad