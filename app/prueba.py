from conexion import *

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route('/prueba')
def prueba():
    nombre = 'juan'
    sql = f"insert into usuario (nombre) values ('{nombre}')"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    return 'exito'



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5080)