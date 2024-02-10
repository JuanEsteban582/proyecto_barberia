
from datetime import timedelta
from random import randint  
from flask import Flask, render_template,redirect,request,session,jsonify
from flask import send_from_directory
from flaskext.mysql import MySQL
import hashlib #para cifrar la contraseña 
from flaskext.mysql import MySQL
from datetime import datetime



app = Flask(__name__)
mysql = MySQL()
app.secret_key=str(randint(10000,99999))  # Necesario para controlar la creación única de sesiones
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes = 30)

app.config['MYSQL_DATABASE_HOST'] ='localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306 #servidor
app.config['MYSQL_DATABASE_USER'] ='root' #el usuario en xampp de administrador
app.config ['MYSQL_DATABASE_PASSWORD'] ='' #contrasaña de la base de datos si le tiene
app.config ['MYSQL_DATABASE_DB'] ='barberia1' 
mysql.init_app(app)