from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/comunidad')
def comunidad():
    return render_template('Comunidad/comunidad.html')

@app.route('/proyectos')
def proyectos():
    return render_template('Proyectos/proyectos.html')

@app.route('/consultoria')
def consultoria():
    return render_template('Consultoria/consultoria.html')

@app.route('/tienda')
def tienda():
    return render_template('Tienda/tienda.html')

@app.route('/blog')
def blog():
    return render_template('Blog/blog.html')

if __name__=='__main__':
    app.run(debug=True)