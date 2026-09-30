from flask import Flask, render_template

# Inicializar la aplicación Flask
app = Flask(__name__)

# Definir la ruta principal (Home)
@app.route('/')
def home():
    # Flask buscará automáticamente dentro de la carpeta "templates"
    return render_template('sgiru_prototipo.html')

# Iniciar el servidor en modo debug
if __name__ == '__main__':
    app.run(debug=True, port=5000)