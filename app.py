from flask import Flask, render_template, request, redirect
import yagmail as yagmail
import utils

app = Flask(__name__)

#Activación de cuenta
@app.route("/")
def principal():
    if request.method == 'POST':
        username = request.form.get('usuario')
        password = request.form['password']
        email = request.form.get('correo')

        if not utils.isUsernameValid(username):
            return render_template('Cover.html')

        if not utils.isPasswordValid(password):
            return render_template('Cover.html')
        
        if not utils.isEmailValid(email):
            return render_template('Cover.html')

        #El correo de donde la aplicación envía el correo
        yag = yagmail.SMTP('laarteaga@uninorte.edu.co','13uninorte31')
        yag.send(to=email, subject='Activa tu cuenta', contents="Bienvenido, usa el siguiente link para activar tu cuenta")
        return redirect('/perfil')


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