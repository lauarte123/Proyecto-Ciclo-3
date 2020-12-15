from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField


class FormInicio(FlaskForm):
    usuario = StringField('Usuario', validators=[DataRequired(message="No dejar vacío")])
    contraseña = PasswordField('Contraseña', validators=[DataRequired(message="No dejar vacío")])
    enviar = SubmitField('Iniciar sesión')

class FormRegistro(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(message="No dejar vacío")])
    apellidos = StringField('Apellidos', validators=[DataRequired(message="No dejar vacío")])
    usuario = StringField('Usuario', validators=[DataRequired(message="No dejar vacío")])
    correo = EmailField('Correo', validators=[DataRequired(message="No dejar vacío")])
    contraseña = PasswordField('Contraseña', validators=[DataRequired(message="No dejar vacío")])
    enviar2 = SubmitField('Registrarse')

class FormContraseña(FlaskForm):
    usuario = StringField('Usuario', validators=[DataRequired(message="No dejar vacío")])
    correo = EmailField('Correo', validators=[DataRequired(message="No dejar vacío")])
    enviar = SubmitField('Enviar')

class FormActualizarUsuario(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(message="No dejar vacío")])
    apellidos = StringField('Apellidos', validators=[DataRequired(message="No dejar vacío")])
    usuario = StringField('Usuario', validators=[DataRequired(message="No dejar vacío")])
    correo = EmailField('Correo', validators=[DataRequired(message="No dejar vacío")])
    contraseñaAnterior = PasswordField('Contraseña anterior', validators=[DataRequired(message="No dejar vacío")])
    contraseñaNueva = PasswordField('Contraseña nueva', validators=[DataRequired(message="No dejar vacío")])
    enviar = SubmitField('Guardar registro') 

class FormEliminarUsuario(FlaskForm):   
    usuario = StringField('Usuario', validators=[DataRequired(message="No dejar vacío")])
    contraseña = PasswordField('Contraseña', validators=[DataRequired(message="No dejar vacío")])
    enviar = SubmitField('Eliminar usuario')