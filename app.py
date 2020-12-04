from flask import Flask, render_template

app = Flask(__name__)

@app.route("/principal")
def principal():
    return render_template(Cover.html)

@app.route("/perfil")
def principal():
    return render_template(Profile.html)

@app.route("/crear")
def crear():
    return render_template(Crear.html)

@app.route("/modificar")
def modificar():
    return render_template(modifical.html)

@app.route("/buscar")
def buscar():
    return render_template(Profile.html)