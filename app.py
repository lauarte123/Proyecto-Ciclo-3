from flask import Flask, render_template, request, redirect
import os
import yagmail as yagmail
import utils
import secrets
from forms import FormInicio, FormRegistro, FormContraseña

app = Flask(__name__)
app.secret_key = os.urandom(24)


#Activación de cuenta
@app.route("/", methods=('GET', 'POST'))
def registro():
    form1 = FormRegistro()
    form2 = FormContraseña()
    form3 = FormInicio()
    if form1.validate_on_submit():
        name = form1.nombre.data
        username = form1.usuario.data
        email = form1.correo.data
        password = form1.contraseña.data

        #El correo de donde la aplicación envía el correo
        yag = yagmail.SMTP('laarteaga@uninorte.edu.co','13uninorte31')
        yag.send(to=email, subject='Activa tu cuenta en Polaroid', contents="Bienvenido, usa el siguiente link para activar tu cuenta")
        return redirect('/')
    return render_template('Cover.html', form_registro=form1, form_contraseña=form2, form_inicio=form3)

@app.route("/recuperar_contraseña", methods=('GET', 'POST'))
def nuevaContraseña():
    form1 = FormRegistro()
    form2 = FormContraseña()
    form3 = FormInicio()
    if form2.validate_on_submit():
        username = form2.usuario.data
        email = form2.correo.data
        
        yag = yagmail.SMTP('laarteaga@uninorte.edu.co','13uninorte31')
        yag.send(to=email, subject='Recuperación de contraseña', contents="Hola, haz clic en el siguiente enlace para recuperar tu contraseña")
        return redirect('/')
    return render_template('Cover.html', form_registro=form1, form_contraseña=form2, form_inicio=form3)
    # return redirect('/')
    # return render_template('Cover.html', form=form)

@app.route("/login", methods=('GET', 'POST'))
def login():
    form1 = FormRegistro()
    form2 = FormContraseña()
    form3 = FormInicio()
    if form3.validate_on_submit():
        username = form3.usuario.data
        password = form3.contraseña.data
        # mensaje = f'Usted ha iniciado sesión con el usuario {username}'
        # flash(mensaje)
        return redirect('/perfil')
    return render_template('Cover.html', form_registro=form1, form_contraseña=form2, form_inicio=form3)

@app.route("/perfil")
def perfil():
    nombre = "Fulanito de Tal"
    correo = "iepenaranda@uninorte.edu.co"
    cantidad = 3
    return render_template('Profile.html', nombre=nombre, correo=correo, cantidad=cantidad)

@app.route("/crear", methods=('GET', 'POST'))
def crear():
    if request.method=="POST":
        return render_template('Crear.html')
    return render_template("Crear.html")

@app.route("/modificar")
def modificar():
    return render_template('modificar.html')

@app.route("/buscar")
def buscar():
    return render_template('search.html')


# Activar el modo debug de la aplicacion
if __name__ == "__main__":
    app.run(debug=True)