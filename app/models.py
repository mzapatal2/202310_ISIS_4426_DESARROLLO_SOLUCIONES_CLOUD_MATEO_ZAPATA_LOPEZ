from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class tabla_usuarios(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), index=True, unique=True)
    password = db.Column(db.String(30), index=True)
    nombre = db.Column(db.String(15), index=True)
    apellido = db.Column(db.String(15), index=True)
    tabla_eventos = db.relationship('tabla_eventos', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.email)

        
    @login.user_loader
    def load_user(id):
        return tabla_usuarios.query.get(int(id))

class tabla_eventos(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre_evento = db.Column(db.String(25))
    categoria = db.Column(db.String(255))
    lugar = db.Column(db.String(25))
    direccion = db.Column(db.String(25))
    fecha_inicio = db.Column(db.DateTime())
    fecha_fin = db.Column(db.DateTime()) 
    evento_presencial = db.Column(db.Integer) 
    fk_usuarios = db.Column(db.Integer, db.ForeignKey('tabla_usuarios.id'))


    def __repr__(self):
        return '<Post {}>'.format(self.body)