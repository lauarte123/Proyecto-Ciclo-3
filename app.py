from flask import Flask, render_template, request, redirect, url_for, \
    flash, session, current_app, g, send_file, make_response, send_from_directory, \
    abort
import os, functools
import yagmail as yagmail
import utils, imghdr
from db import get_db, close_db
from forms import FormInicio, FormRegistro, FormContraseña, FormActualizarUsuario, FormEliminarUsuario, SubirImagen, ActualizarImagen
from functools import wraps
import sqlite3
from sqlite3 import Error
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = "./Archivos"
app.config['UPLOAD_PATH'] = 'Archivos'
app.config['MAX_CONTENT_LENGTH'] = 7 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.PNG','.JPG','.GIF']

#Función decoradora para validar el login
def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwds):
        if g.user is None:
            return redirect(url_for('login'))
        return view(*args, **kwds)
    return wrapped_view

@app.route('/')
def principal():
    form1 = FormRegistro()
    form2 = FormContraseña()
    form3 = FormInicio()
    if g.user:
        return redirect( url_for( 'perfil' ) )
    return render_template('Cover.html', form_registro=form1, form_contraseña=form2, form_inicio=form3)

#Activación de cuenta
@app.route('/registro/', methods=('GET', 'POST'))
def registro():
    try:
        form1 = FormRegistro()
        form2 = FormContraseña()
        form3 = FormInicio()

        if form1.validate_on_submit():
            db = get_db()

            nombres = form1.nombre.data
            apellidos = form1.apellidos.data
            usuario = form1.usuario.data
            email = form1.correo.data
            contraseña = form1.contraseña.data

            hash_contraseña = generate_password_hash(contraseña)

            db.execute('insert into usuario (Usuario, Nombres, Apellidos, Correo, Contraseña) values(?,?,?,?,?)', (usuario, nombres, apellidos, email, hash_contraseña))
            db.commit()

            yag = yagmail.SMTP('laarteaga@uninorte.edu.co','13uninorte31')
            yag.send(to=email, subject="Activa tu cuenta en Polaroid", contents="Bienvenido, usa el siguiente link para activar tu cuenta")
            return redirect('/')
        return render_template('Cover.html', form_registro=form1, form_contraseña=form2, form_inicio=form3)
    
    except Error:
        return Error

@app.route("/recuperar_contraseña", methods=('GET', 'POST'))
def nuevaContraseña():
    form1 = FormRegistro()
    form2 = FormContraseña()
    form3 = FormInicio()
    if form2.validate_on_submit():

        db = get_db()
        usuario = form2.usuario.data
        email = form2.correo.data
        error = None
        user = db.execute('SELECT * FROM usuario WHERE usuario = ?', (usuario,)).fetchone()

        if user is None:
            error = "Usuario inválido"
        else:
            correo = user['Correo']
            yag = yagmail.SMTP('laarteaga@uninorte.edu.co','13uninorte31')
            yag.send(to=str(correo), subject="POLAROID: Recuperación de contraseña", contents="Hola, haz clic en el siguiente enlace para recuperar tu contraseña")
            return redirect('/')
        
        return error

        #listaUsuario = sql_select_usuarios()
        #tamañoLista=len(listaUsuario)

        #for i in range (tamañoLista):
            #if usuario==listaUsuario[i][0] and email==listaUsuario[i][3]:
                #yag = yagmail.SMTP('laarteaga@uninorte.edu.co','13uninorte31')
                #yag.send(to=email, subject='Recuperación de contraseña', contents="Hola, haz clic en el siguiente enlace para recuperar tu contraseña")
                #return redirect('/')
            #else:
                #continue
        #return ("Usuario no encontrado")
        
    return render_template('Cover.html', form_registro=form1, form_contraseña=form2, form_inicio=form3)
    

@app.route("/login", methods=('GET', 'POST'))
def login():
    try:
        form1 = FormRegistro()
        form2 = FormContraseña()
        form3 = FormInicio()
        if g.user:
            return redirect(url_for('perfil'))
        if request.method == 'POST':
            db = get_db()
            
            error = None
            # if form3.validate_on_submit():
            usuario = form3.usuario.data
            contraseña = form3.contraseña.data
            # return('cualquier cosa')
            user = db.execute('SELECT * FROM usuario WHERE usuario = ?', (usuario, )).fetchone()

            if user is None:
                error = 'Usuario o contraseña inválidos'
            else:
                if check_password_hash(user['Contraseña'], contraseña):
                    session.clear()
                    session['usuario'] = user[0]
                    resp = make_response(redirect( url_for('perfil') ))
                    resp.set_cookie('usuario', usuario)
                    return resp
            flash(error)
        return render_template('Cover.html', form_registro=form1, form_contraseña=form2, form_inicio=form3)
    except Error:
        print(Error)
        return('Error')
        # return render_template('Cover.html', form_registro=form1, form_contraseña=form2, form_inicio=form3)


@app.route("/perfil", methods=('GET', 'POST'))
@login_required
def perfil():
    form1 = FormActualizarUsuario()
    form2 = FormEliminarUsuario()
    db = get_db()
    if g.user:
        nombre = g.user['Nombres']
        correo = g.user['Correo']
        usuario = request.cookies.get('usuario')
        return render_template('Profile.html', nombre=nombre, correo=correo, form_actualizar_usuario=form1, form_eliminar_usuario=form2)

    return render_template('Profile.html', nombre=nombre, correo=correo, form_actualizar_usuario=form1, form_eliminar_usuario=form2)


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

### Visualizar imágenes y rutas guardadas en Archivos
@app.route('/verArchivos/')
def ver():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('ver.html', files=files)

###
@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

### Validación de la imagen
def validate_image(stream):
    header = stream.read(512)  # 512 bytes should be enough for a header check
    stream.seek(0)  # reset stream pointer
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@app.route("/crear/", methods=('GET', 'POST'))
def crear():
    form = SubirImagen()
    if request.method == 'GET':
        return render_template("Crear.html", form_subir=form)
    else:
        f = request.files['archivo']  # obtenemos el archivo del input "archivo"
        filename = secure_filename(f.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                file_ext != validate_image(f.stream): 
                return "Invalid image", 400    
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # Guardamos el archivo en el directorio "Archivos "
        
        if form.validate_on_submit():
            nombre = form.nombre.data
            descripcion = form.descripcion.data
            privacidad = str(form.privacidad.data)
            usuario = session['usuario'] 
            sql_insert_imagen(usuario, nombre, descripcion, privacidad, filename)
            return redirect('/perfil')
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
def sql_insert_imagen(id_usuario, nombre, descripcion, privada, ruta):
    query = "INSERT INTO Imagen (Id_usuario, Nombre_imagen, Descripcion, Privada, Ruta) VALUES ('"+id_usuario+"','"+nombre+"','"+descripcion+"',"+privada+",'"+ruta+"');"
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


@app.before_request
def load_logged_in_user():
    usuario = session.get('usuario') 
    if usuario is None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM usuario WHERE usuario = ?', (usuario,)).fetchone()


# Limpia la variable de sesión y redirige a la página principal
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('principal'))

# Subir imagen
@app.route("/")
def upload_file():
 return render_template('Crear.html')

# Descargar imagen
@app.route('/downloadimage/')
def downloadimage():
    return send_file('static/img/image (1).jpg',as_attachment=True)

# Activar el modo debug de la aplicacion
if __name__ == "__main__":
    app.run(debug=True)