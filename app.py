from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'sgiru_secreto_123'

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

# Modelo de Usuarios
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(50), default='estudiante')

# Modelo de Reservas
class Reserva(db.Model):
    __tablename__ = 'reservas'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    recurso_id = db.Column(db.Integer, db.ForeignKey('recursos.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    estado = db.Column(db.String(50), default='activa')

@app.route('/')
def home():
    lista_recursos = Recurso.query.all()
    usuario_actual = session.get('usuario') 
    return render_template('sgiru_prototipo.html', recursos_db=lista_recursos, usuario=usuario_actual)

@app.route('/login', methods=['POST'])
def login():
    correo_form = request.form['correo']
    password_form = request.form['password']
    
    usuario = Usuario.query.filter_by(correo=correo_form, password_hash=password_form).first()
    if usuario:
        session['usuario'] = {'id': usuario.id, 'correo': usuario.correo, 'rol': usuario.rol}
    
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('home'))

@app.route('/reservar', methods=['POST'])
def reservar():
    if 'usuario' not in session:
        return redirect(url_for('home'))
        
    # Recibir datos del formulario HTML
    recurso_id = request.form['recurso_id']
    fecha = request.form['fecha']
    hora_inicio = request.form['hora_inicio']
    hora_fin = request.form['hora_fin']
    usuario_id = session['usuario']['id']

    # Crear la reserva en MySQL
    nueva_reserva = Reserva(
        usuario_id=usuario_id,
        recurso_id=recurso_id,
        fecha=fecha,
        hora_inicio=hora_inicio,
        hora_fin=hora_fin
    )
    db.session.add(nueva_reserva)
    
    # Cambiar el estado del recurso para que aparezca como ocupado
    recurso = Recurso.query.get(recurso_id)
    if recurso:
        recurso.estado = 'inactivo'
        
    db.session.commit() # Guardar los cambios definitivamente
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)