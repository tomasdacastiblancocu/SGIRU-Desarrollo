from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'sgiru_secreto_123' # Requisito obligatorio para usar variables de sesión

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/sgiru_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de Recursos
class Recurso(db.Model):
    __tablename__ = 'recursos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    req_software = db.Column(db.String(100))
    req_hardware = db.Column(db.String(100))
    estado = db.Column(db.String(50), default='activo')

# Nuevo: Modelo de Usuarios
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(50), default='estudiante')

@app.route('/')
def home():
    lista_recursos = Recurso.query.all()
    # Enviamos la variable de sesión al HTML para saber si mostramos el login o la app
    usuario_actual = session.get('usuario') 
    return render_template('sgiru_prototipo.html', recursos_db=lista_recursos, usuario=usuario_actual)

@app.route('/login', methods=['POST'])
def login():
    correo_form = request.form['correo']
    password_form = request.form['password']
    
    # Buscar en MySQL si el correo y la contraseña coinciden
    usuario = Usuario.query.filter_by(correo=correo_form, password_hash=password_form).first()
    
    if usuario:
        # Guardar datos en la sesión del navegador
        session['usuario'] = {'id': usuario.id, 'correo': usuario.correo, 'rol': usuario.rol}
    
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    # Eliminar al usuario de la sesión
    session.pop('usuario', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)