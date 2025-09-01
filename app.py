from flask import Flask, render_template, session, request, redirect
from typing import Any, Optional
from acceso_db import AccesoDB
from constante import ADB
import pymysql as db
from pymysql.cursors import DictCursor

app = Flask(__name__)
app.secret_key = 'supersecreta'

accesoDB = AccesoDB("127.0.0.1","root", "", "agenda")   

@app.route("/", methods = ['GET','POST'])
def home():
    if 'user' in session:
        return render_template("home.html", titulo="Formulario")
    if 'saludo' not in session:
        session['saludo'] = False
    if 'error' not in session:
        session['error'] = False
    return render_template("login.html", error=session['error'], saludo=session['saludo'])

@app.route("/admin", methods = ['GET','POST'])
def admin():
    if 'user' in session:
        return render_template("admin.html", titulo="Formulario")
    if 'saludo' not in session:
        session['saludo'] = False
    if 'error' not in session:
        session['error'] = False
    return render_template("login.html", error=session['error'], saludo=session['saludo'])

@app.route("/nuevo", methods=['POST'])
def nuevo_contacto():
    nom = request.form['nombre']
    mail = request.form['mail']
    tel = request.form['telefono']
    ig = request.form['ig']
    accesoDB.crear("agenda", {"usuario":session['user'], "nombre":nom, "mail":mail,"numero":tel,"ig":ig})
    return render_template("home.html", titulo="Formulario", nuevo=True)

@app.route("/nuevou", methods=['POST'])
def nuevo_usuario():
    user = request.form['usuario']
    password = request.form['contraseña']
    accesoDB.crear("usuarios", {"usuario": user,"contraseña":password})
    return render_template("admin.html", titulo="Formulario", nuevou=True)

@app.route("/buscar", methods=['POST'])
def buscar_contacto():
    big = request.form['ig']
    resultado=accesoDB.obtener("agenda", ["nombre","mail","numero","ig"],filtro=("ig",big))
    if resultado:
        contacto = resultado[0]
        return render_template("home.html", titulo="Formulario", nombrebuscar=contacto)
    else:
        return render_template("home.html", titulo="Formulario", nombrebuscar=None, no_encontrado=True)

@app.route("/borrar", methods=['POST'])
def borrar_contacto():
    dig = request.form['ig']
    accesoDB.borrar("agenda", ("ig",dig))
    return render_template("home.html", titulo="Formulario", borrar = True)

@app.route("/borraru", methods=['POST'])
def borrar_usuario():
    duser = request.form['usuario']
    accesoDB.borrar("usuarios", ("usuario",duser))
    return render_template("admin.html", titulo="Formulario", borraru = True)

@app.route("/login", methods = ['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    usuarioLista=accesoDB.obtener("usuarios", ["usuario","contraseña"],filtro=("usuario", username))
    usuario=usuarioLista[0]
    if username == 'admin' and password == usuario['contraseña']:
        session['user'] = 'admin'
        return redirect("/admin")
    if username == usuario['usuario'] and password == usuario['contraseña']:
        session['user'] = username
        return redirect("/")   
    session['error'] = True
    return redirect("/")

@app.route("/logout", methods = ['POST'])
def logout():
    session.clear()
    session['saludo'] = True
    return redirect("/")

if __name__ == "__main__":
    app.run()
