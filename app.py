from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de conexión a MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/sgiru_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo que mapea la tabla 'recursos' de MySQL
class Recurso(db.Model):
    __tablename__ = 'recursos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    req_software = db.Column(db.String(100))
    req_hardware = db.Column(db.String(100))
    estado = db.Column(db.String(50), default='activo')

@app.route('/')
def home():
    # 1. Consultar todos los recursos en la base de datos
    lista_recursos = Recurso.query.all()
    
    # 2. Enviar los datos al HTML usando la variable 'recursos_db'
    return render_template('sgiru_prototipo.html', recursos_db=lista_recursos)

if __name__ == '__main__':
    app.run(debug=True, port=5000)