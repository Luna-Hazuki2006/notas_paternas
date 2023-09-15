from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'pBsMG9T=Vjz*yDb}64$twh'

@app.route('/')
def iniciar():
    return render_template('/inicio/index.html')

if __name__ == '__main__':
    app.run(debug=True)