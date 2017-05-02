from flask import render_template, flash, redirect, session, url_for, request, g, current_app
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.principal import Identity, AnonymousIdentity, identity_changed, RoleNeed, UserNeed, identity_loaded
from app.model.user import Usuario
from app import app, db, lm, principals
from .acceso import Login
from datetime import datetime
from pytz import timezone


@lm.user_loader
def load_user(id):
    return Usuario.query.get(id)

@app.before_request
def before_request():
    g.user = current_user

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'usu_login'):
        identity.provides.add(UserNeed(current_user.usu_login))

    # update the identity with the rol that the user provides
    if hasattr(current_user, 'usu_rol'):
        for rol in current_user.usu_rol.split('-'):
            identity.provides.add(RoleNeed(rol))

@app.route('/acceder', methods=['GET', 'POST'])
def login():
    datos = {'title' : 'Facturación Casa Luifer'}
    form = Login()
    if form.validate_on_submit():
        user = Usuario.query.get(form.usuario.data)
        if user is not None and user.usu_password == form.clave.data and user.usu_estado == 1:
            session['remember_me'] = form.recordarme.data
            login_user(user)

            # Tell Flask-Principal the identity changed
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.usu_login))


            #Modificar fecha de acceso del usuario actual
            Usuario.query.filter(Usuario.usu_login == user.usu_login).update({Usuario.usu_acceso: datetime.now(timezone('America/Bogota'))}, synchronize_session=False)
            db.session.commit()

            return redirect('/pedidos')

    return render_template('identifica.html',
                           datos = datos,
                           form = form)

@app.route('/salir')
def logout():
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())

    return redirect('/acceder')


####Prueba#####
@app.teardown_request
def session_clear(exception=None):
    db.session.remove()
    if exception and db.session.is_active:
        db.session.rollback()