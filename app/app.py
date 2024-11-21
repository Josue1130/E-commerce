from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hombre')
def hombre():
    return render_template('hombre.html')

@app.route('/mujer')
def mujer():
    return render_template('mujer.html')

@app.route('/niño')
def nino():
    return render_template('niño.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
