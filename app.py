from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de conexión a MySQL (usuario 'root', sin contraseña, base de datos 'sgiru_db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/sgiru_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar el ORM
db = SQLAlchemy(app)

@app.route('/')
def home():
    return render_template('sgiru_prototipo.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)