from flask import render_template, flash, redirect, session, url_for
from sqlalchemy import Engine, asc, desc, update
from app import app
from app.forms import EventoForm, LoginForm
from flask_login import current_user, login_user
from app.models import tabla_eventos, tabla_usuarios
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = EventoForm()
    if form.validate_on_submit():
        evento = tabla_eventos(id=form.id.data, nombre_evento=form.nombre_evento.data, categoria=form.categoria.data, lugar=form.lugar.data, direccion=form.direccion.data, evento_presencial=form.evento_presencial.data, fk_usuarios=current_user.get_id())
        db.session.add(evento)
        db.session.commit()
        flash('Congratulations, you registered an event!')
        return redirect(url_for('index'))
    eventos = tabla_eventos.query.filter(tabla_eventos.fk_usuarios == current_user.get_id()).order_by(desc(tabla_eventos.id))
    return render_template("index.html", title='Home Page', eventos=eventos, form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = tabla_usuarios.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = tabla_usuarios(email=form.email.data, nombre=form.nombre.data, apellido=form.apellido.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/evento_detalle', methods=['GET', 'POST', 'DELETE'])
def evento_detalle():
    if current_user.is_authenticated:
        mostrar_evento = tabla_eventos.query.filter(tabla_eventos.fk_usuarios == current_user.get_id()).order_by(desc(tabla_eventos.id))
        form = EventoForm()
        select = request.args.get('evento_detalle')
        if select != None:
            evento_buscado = tabla_eventos.query.filter(tabla_eventos.id == select)[0]
            form = EventoForm(id=evento_buscado.id, nombre_evento=evento_buscado.nombre_evento, categoria=evento_buscado.categoria, lugar=evento_buscado.lugar, direccion=evento_buscado.direccion, evento_presencial=evento_buscado.evento_presencial)
            flash('Este es el evento seleccionado!')
        else:
            evento_buscado = tabla_eventos()
        if form.delete.data:
            eliminar = form.id.data
            if eliminar != None:
                tabla_eventos.query.filter(tabla_eventos.id == int(eliminar)).delete()
                db.session.commit()
                flash('Evento eliminado!')
            else:
                evento_buscado = tabla_eventos()
            return redirect(url_for('evento_detalle', form=form)) 
            
        if form.validate_on_submit():
                actualizar = form.id.data
                tabla_eventos.query.filter(tabla_eventos.id == int(actualizar)).update({"nombre_evento" : form.nombre_evento.data, "categoria" : form.categoria.data, "lugar" : form.lugar.data, "direccion" : form.direccion.data, "direccion" : form.direccion.data, "evento_presencial" : form.evento_presencial.data})
                db.session.flush()
                db.session.commit()
                flash('Your changes have been saved.')
        return render_template('evento_detalle.html', mostrar_evento=mostrar_evento, form=form)
    return render_template('login.html', title='Sign In')


