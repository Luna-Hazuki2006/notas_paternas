import pymongo

cliente = pymongo.MongoClient('mongodb+srv://lunahazuki2006:cXU0lYhSncWZ12FM@cluster0.owjghpf.mongodb.net/')

db = cliente.notas_paternas

categorias = db.categorias
notas = db.notas
examenes = db.examenes