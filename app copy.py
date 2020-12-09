from flask import Flask, render_template, request, redirect
import os
import yagmail as yagmail
import utils
import secrets
from forms import FormInicio 

app = Flask(__name__)
app.secret_key = os.urandom(24)
# secret_key = secrets.token_hex(16)
# app.config['SECRET_KEY'] = secret_key

#Activación de cuenta
@app.route("/", methods=('GET', 'POST'))
def registro():
    form = FormInicio()
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        if not utils.isUsernameValid(name):
            return render_template('Cover.html')

        if not utils.isUsernameValid(username):
            return render_template('Cover.html')

        if not utils.isPasswordValid(password):
            return render_template('Cover.html')
        
        if not utils.isEmailValid(email):
            return render_template('Cover.html')

        #El correo de donde la aplicación envía el correo
        yag = yagmail.SMTP('laarteaga@uninorte.edu.co','13uninorte31')
        yag.send(to=email, subject='Activa tu cuenta en Polaroid', contents="Bienvenido, usa el siguiente link para activar tu cuenta")
        return redirect('/')
    return render_template('Cover.html')

@app.route("/recuperar_contraseña", methods=('GET', 'POST'))
def nuevaContraseña():
    if request.method == 'POST':
        email = request.form.get('email')
        
        if not utils.isEmailValid(email):
            return render_template('Cover.html')
        yag = yagmail.SMTP('laarteaga@uninorte.edu.co','13uninorte31')
        yag.send(to=email, subject='Recuperación de contraseña', contents="Hola, haz clic en el siguiente enlace para recuperar tu contraseña")
        return redirect('/')

@app.route("/login", methods=('GET', 'POST'))
def login():
    form = FormInicio()
    if form.validate_on_submit():
        username = form.usuario.data
        # mensaje = f'Usted ha iniciado sesión con el usuario {username}'
        # flash(mensaje)
        return redirect('/perfil')
    return render_template('Cover.html', form=form)

@app.route("/perfil")
def perfil():
    nombre = "Fulanito de Tal"
    correo = "iepenaranda@uninorte.edu.co"
    cantidad = 3
    return render_template('Profile.html', nombre=nombre, correo=correo, cantidad=cantidad)

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