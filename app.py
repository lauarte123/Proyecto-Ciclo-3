from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def principal():
    return render_template('Cover.html')

@app.route("/perfil")
def perfil():
    return render_template('Profile.html')

@app.route("/crear")
def crear():
    return render_template('Crear.html')

@app.route("/modificar")
def modificar():
    return render_template('modificar.html')

@app.route("/buscar")
def buscar():
    return render_template('search.html')

# Activar el modo debug de la aplicacion
if __name__ == "__main__":
    app.run(debug=True)