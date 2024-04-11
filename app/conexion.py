
from datetime import timedelta
from random import randint  
from flask import Flask, render_template,redirect,request,session,jsonify,url_for
from flask import send_from_directory
from flaskext.mysql import MySQL
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
mysql = MySQL()
app.secret_key=str(randint(10000,99999))  # Necesario para controlar la creación única de sesiones
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes = 30)

app.config['MYSQL_DATABASE_HOST'] ='localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306 #servidor
app.config['MYSQL_DATABASE_USER'] ='id22030536_barberlocate' #el usuario en xampp de administrador
app.config ['MYSQL_DATABASE_PASSWORD'] ='Barber_locate1234' #contrasaña de la base de datos si le tiene
app.config ['MYSQL_DATABASE_DB'] ='id22030536_barberia1' 
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
mysql.init_app(app)