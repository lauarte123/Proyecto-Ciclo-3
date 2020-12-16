from flask import Flask, render_template, request, redirect, flash
import os
import yagmail as yagmail
import utils
from forms import FormInicio, FormRegistro, FormContraseña, FormActualizarUsuario, FormEliminarUsuario, SubirImagen, ActualizarImagen
import sqlite3
from sqlite3 import Error

#from werkzeug import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = "./Archivos"

#Activación de cuenta
@app.route("/", methods=('GET', 'POST'))
def registro():
    form1 = FormRegistro()
    form2 = FormContraseña()
    form3 = FormInicio()

    if form1.validate_on_submit():
        nombres = form1.nombre.data
        apellidos =form1.apellidos.data
        usuario = form1.usuario.data
        email = form1.correo.data
        contraseña = form1.contraseña.data

        sql_insert_usuarios(usuario, nombres, apellidos, email, contraseña)

        
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
        usuario = form2.usuario.data
        email = form2.correo.data
        listaUsuario = sql_select_usuarios()
        tamañoLista=len(listaUsuario)
        for i in range (tamañoLista):
            if usuario==listaUsuario[i][0] and email==listaUsuario[i][3]:
                yag = yagmail.SMTP('laarteaga@uninorte.edu.co','13uninorte31')
                yag.send(to=email, subject='Recuperación de contraseña', contents="Hola, haz clic en el siguiente enlace para recuperar tu contraseña")
                return redirect('/')
            else:
                continue
        return ("Usuario no encontrado")
        
        
    return render_template('Cover.html', form_registro=form1, form_contraseña=form2, form_inicio=form3)
    

@app.route("/login", methods=('GET', 'POST'))
def login():
    form1 = FormRegistro()
    form2 = FormContraseña()
    form3 = FormInicio()
    if form3.validate_on_submit():
        usuario = form3.usuario.data
        contraseña = form3.contraseña.data
        listaUsuario = sql_select_usuarios()
        tamañoLista=len(listaUsuario)
        for i in range (tamañoLista):
            if usuario==listaUsuario[i][0] and contraseña==listaUsuario[i][4]:
                return redirect('/perfil')
            else:
                continue
        return ("Vuelve a intentarlo")
        # mensaje = f'Usted ha iniciado sesión con el usuario {username}'
        # flash(mensaje)
    return render_template('Cover.html', form_registro=form1, form_contraseña=form2, form_inicio=form3)


@app.route("/perfil")
def perfil():
    form1 = FormActualizarUsuario()
    form2 = FormEliminarUsuario()
    nombre = "Fulanito de Tal"
    correo = "iepenaranda@uninorte.edu.co"
    cantidad = 3
    return render_template('Profile.html', nombre=nombre, correo=correo, cantidad=cantidad, form_actualizar_usuario=form1, form_eliminar_usuario=form2)

@app.route("/actualizarInformacion", methods=('GET', 'POST'))
def actualizarInformacion():
    form = FormActualizarUsuario()
    if form.validate_on_submit():
        nombres = form.nombre.data
        apellidos =form.apellidos.data
        usuario = form.usuario.data
        email = form.correo.data
        contraseñaAnterior = form.contraseñaAnterior.data
        contraseñaNueva = form.contraseñaNueva.data
        #Validación datos usuario
        listaUsuario = sql_select_usuarios()
        tamañoLista=len(listaUsuario)
        for i in range (tamañoLista):
            if usuario == listaUsuario[i][0] and contraseñaAnterior == listaUsuario[i][4]:
                sql_edit_usuarios(usuario, nombres, apellidos, email, contraseñaNueva)
                mensaje = 'Su información de ha sido actualizada correctamente'
                flash(mensaje)
                return redirect('/perfil')
            else:
                continue
    return redirect('/perfil')
        

@app.route("/eliminar_usuario", methods=('GET', 'POST'))
def eliminar_usuario():
    form = FormEliminarUsuario()
    if form.validate_on_submit():
        usuario = form.usuario.data
        contraseña = form.contraseña.data

        listaUsuario = sql_select_usuarios()
        tamañoLista=len(listaUsuario)
        for i in range (tamañoLista):
            if usuario == listaUsuario[i][0] and contraseña == listaUsuario[i][4]:
                sql_delete_usuarios(usuario)
                # mensaje = 'Su información de ha sido actualizada correctamente'
                # flash(mensaje)
                return redirect('/')
            else:
                continue
    return redirect('/perfil')


@app.route("/crear", methods=('GET', 'POST'))
def crear():
    form = SubirImagen()
    if form.validate_on_submit():
        nombre = form.nombre.data
        descripcion = form.descripcion.data
        privacidad = str(form.privacidad.data)
        usuario = "iepenaranda"
        sql_insert_imagen(usuario, nombre, descripcion, privacidad)
        
        return redirect("/perfil")

    return render_template("Crear.html", form_subir=form)

@app.route("/modificar")
def modificar():
    return render_template('modificar.html')

@app.route('/buscar/<string:busqueda>/', methods=('GET', 'POST'))
def buscar(busqueda):
    if request.method == "POST":
        postInput = request.form.get("busqueda")
        return render_template('search.html', busqueda=postInput)
    elif request.method == "GET":
        return render_template('search.html', busqueda=busqueda)

### CONEXIÓN A BASE DE DATOS ###

def sql_connection():
    try:
        con = sqlite3.connect('database.db')
        return con
    except Error:
        print(Error)

def sql_insert_usuarios(usuario, nombres, apellidos, correo, contraseña):
    query = "insert into usuario (Usuario, Nombres, Apellidos, Correo, Contraseña) values ('" + usuario + "', '" + nombres + "', '" + apellidos + "', '" + correo + "', '" + contraseña +"');"
    try:
        con = sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(query)
        con.commit()
        con.close()
    except Error:
        print(Error)

@app.route('/prueba')
def prueba():
    usuarios = sql_select_usuarios()
    return render_template('productos.html', productos=usuarios)


def sql_select_usuarios():
    query = "select * from usuario;"
    try: 
        con = sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(query)
        usuarios = cursorObj.fetchall()
        con.close()
        return usuarios
    except Error:
        print(Error)

def sql_edit_usuarios(usuario, nombres, apellidos, correo, contraseña):
    query = "update usuario set nombres='" + nombres + "', apellidos='" + apellidos + "', correo= '" + correo+ "', contraseña = '" + contraseña + "' where usuario = '"+ usuario + "';"
    try:
        con = sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(query)
        con.commit()
        con.close()
    except Error:
        print(Error)

def sql_delete_usuarios(usuario):
    query = "delete from usuario where usuario = '" + usuario + "';"
    try:
        con = sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(query)
        con.commit()
        con.close()
    except Error:
        print(Error)


#------------- CRUD de las imágenes  --------------------
def sql_insert_imagen(id_usuario, nombre, ruta, privada):
    query = "INSERT INTO Imagen (Id_usuario, Nombre_imagen, Ruta_guardar, Privada) VALUES ('"+id_usuario+"','"+nombre+"','"+ruta+"',"+privada+");"
    try:
        con = sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(query)
        con.commit()
        con.close()
    except Error:
        print(Error)

def sql_select_imagen(id):
    query = "SELECT * FROM Imagen WHERE Id_imagen="+id+";"
    try:
        con = sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(query)
        imagen = cursorObj.fetchall()
        con.close()
        return imagen
    except Error:
        print(Error)

def sql_select_imagenes():
    query = "SELECT * FROM Imagen;"
    try:
        con = sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(query)
        imagenes = cursorObj.fetchall()
        con.close()
        return imagenes
    except Error:
        print(Error)

def sql_update_imagen(id,nombre,privada):
    query = "UPDATE Imagen SET Nombre_imagen='"+nombre+"', privada="+privada+" WHERE Id_imagen="+id+";"
    try:
        con = sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(query)
        con.commit()
        con.close()
    except Error:
        print(Error)

def sql_delete_imagen(id):
    query = "DELETE FROM Imagen WHERE Id_imagen="+id+";"
    try:
        con = sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(query)
        con.commit()
        con.close()
    except Error:
        print(Error)

# Activar el modo debug de la aplicacion
if __name__ == "__main__":
    app.run(debug=True)