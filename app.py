from flask import Flask, render_template
from db import categorias, notas, examenes

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'pBsMG9T=Vjz*yDb}64$twh'

@app.route('/')
def iniciar():
    return render_template('/inicio/index.html')

@app.route('/pregunta')
def listar_preguntas():
    return render_template('/pregunta/index.html')

@app.route('/categoria')
def listar_categorias():
    return render_template('/pregunta/index.html')

@app.route('/examenes')
def listar_examenes(): 
    return render_template('/examenes/index.html')

if __name__ == '__main__':
    app.run(debug=True)