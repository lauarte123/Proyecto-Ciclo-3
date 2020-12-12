from flask import Flask, render_template, request, redirect
import os
import yagmail as yagmail
import utils
import secrets
from forms import FormInicio, FormRegistro, FormContraseña
import sqlite3
from sqlite3 import Error


app = Flask(__name__)
app.secret_key = os.urandom(24)


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
    nombre = "Fulanito de Tal"
    correo = "iepenaranda@uninorte.edu.co"
    cantidad = 3
    return render_template('Profile.html', nombre=nombre, correo=correo, cantidad=cantidad)

@app.route("/crear", methods=('GET', 'POST'))
def crear():
    return render_template("Crear.html")

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

def sql_edit_usuarios(id, usuario, nombres, apellidos, correo, contraseña):
    query = "update usuario set usuario='" + usuario + "', nombres='" + nombres + "', apellidos='" + apellidos + "', correo= '" + correo+ "', contraseña = '" + contraseña + "' where id = "+ id + ";"
    try:
        con = sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(query)
        con.commit()
        con.close()
    except Error:
        print(Error)

def sql_delete_usuarios(id):
    query = "delete from usuario where id = " + id + ";"
    try:
        con = sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(query)
        con.commit()
        con.close()
    except Error:
        print(Error)

# @app.route("/productos")
# def productos():
#     productos = sql_select_productos()
#     return render_template('productos.html', productos=productos)

# @app.route("/crearProducto", methods=('GET', 'POST'))
# def crearProducto():
#     if request.method == 'GET':
#         form = Producto() #Formulario para recoger la info del prod
#         return render_template('nuevo_producto.html', form=form)
#     else:
#         nombre = request.form.get('nombre')
#         precio = request.form['precio']
#         existencia = request.form['existencia']
#         sql_insert_productos(nombre, precio, existencia)
#         return 'OK'

# @app.route("/editarProducto")
# # @app.route("/editarProducto", methods=('GET'))
# def editarProducto():
#     id = request.args.get('id')
#     nombre = request.args.get('nombre')
#     precio = request.args.get('precio')
#     existencia = request.args.get('existencia')
#     sql_edit_producto(id, nombre, precio, existencia)
#     return 'OK'

# @app.route("/eliminarProducto")
# # @app.route("/eliminarProducto", methods=('GET'))
# def eliminarProducto():
#     id = request.args.get('id')
#     sql_delete_producto(id)
#     return 'OK'

#HOLA MUNDO

# Activar el modo debug de la aplicacion
if __name__ == "__main__":
    app.run(debug=True)