from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configuración de la base de datos
app.secret_key = 'clave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tienda.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(80), nullable=False)
    apellidos = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    contraseña = db.Column(db.String(120), nullable=False)

# Modelo de Producto
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    imagen = db.Column(db.String(120), nullable=False)
    genero = db.Column(db.String(20), nullable=False)  # Nuevo campo para género

# Rutas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contraseña = request.form['password']
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.contraseña == contraseña:  # Comparar directamente las contraseñas
            session['usuario_id'] = usuario.id
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Correo o contraseña incorrectos.', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        email = request.form['email']
        telefono = request.form['telefono']
        contraseña = request.form['password']
        confirmar_contraseña = request.form['confirmar-password']

        if contraseña != confirmar_contraseña:
            flash('Las contraseñas no coinciden.', 'error')
            return redirect(url_for('register'))

        nuevo_usuario = Usuario(
            nombres=nombres, 
            apellidos=apellidos, 
            email=email, 
            telefono=telefono, 
            contraseña=contraseña  # Contraseña almacenada en texto claro
        )

        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash('Registro exitoso. Por favor inicia sesión.', 'success')
            return redirect(url_for('login'))
        except:
            flash('El correo ya está registrado.', 'error')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('usuario_id', None)
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('index'))

# Rutas de productos
@app.route('/hombre')
def hombre():
    productos = Producto.query.filter_by(genero='hombre').all()  # Filtra por género 'hombre'
    return render_template('hombre.html', productos=productos)

@app.route('/mujer')
def mujer():
    productos = Producto.query.filter_by(genero='mujer').all()  # Filtra por género 'mujer'
    return render_template('mujer.html', productos=productos)

@app.route('/nino')
def nino():
    productos = Producto.query.filter_by(genero='nino').all()  # Filtra por género 'niño'
    return render_template('nino.html', productos=productos)


# Ruta para agregar productos al carrito
@app.route('/agregar_al_carrito/<int:id>')
def agregar_al_carrito(id):
    producto = Producto.query.get_or_404(id)
    
    if 'carrito' not in session:
        session['carrito'] = []
    
    # Agregar el producto al carrito
    session['carrito'].append({
        'id': producto.id,
        'nombre': producto.nombre,
        'precio': producto.precio,
        'imagen': producto.imagen
    })
    
    flash(f'{producto.nombre} ha sido agregado al carrito.', 'success')
    return redirect(url_for('hombre'))  # Cambia la redirección al lugar que prefieras

# Ruta para mostrar el carrito
@app.route('/carrito')
def carrito():
    carrito = session.get('carrito', [])
    return render_template('carrito.html', carrito=carrito)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas si no existen
    app.run(debug=True)
