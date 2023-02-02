from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import tabla_usuarios

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    nombre = StringField('nombre', validators=[DataRequired()])
    apellido = StringField('apellido', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = tabla_usuarios.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EventoForm(FlaskForm):
    id = IntegerField('id', validators=[DataRequired()])
    nombre_evento = StringField('nombre_evento', validators=[DataRequired()])
    categoria = SelectField('categoria', choices=['Conferencia', 'Seminario', 'Congreso', 'Curso'], validators=[DataRequired()])
    lugar = StringField('lugar')
    direccion = StringField('direccion')
    fecha_inicio = DateField('fecha_inicio')
    fecha_fin = DateField('fecha_fin')
    evento_presencial = SelectField('evento_presencial', choices=[0, 1])
    submit = SubmitField('Submit')
    delete = SubmitField('delete')