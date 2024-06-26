from conexion import *
from datetime import datetime
from flask import flash

#LOGIN O INICIO DE SESION 


@app.route('/')
def index():
    session["logueado"] = False
    return render_template('login.html')

@app.route("/login", methods=['POST'])
def login():
    email = request.form['correo_user']
    contrasena = request.form['contrasena']

    conn = mysql.connect()
    cursor = conn.cursor()

    sql_usuario = f"SELECT contrasena,correo FROM usuario WHERE correo='{email}'"
    cursor.execute(sql_usuario)
    resultado_usuario = cursor.fetchone()

    
    sql_barbero = f"SELECT bcontrasena,bcorreo FROM barberos WHERE bcorreo='{email}'"
    cursor.execute(sql_barbero)
    resultado_barbero = cursor.fetchone()

    
    sql_propietario = f"SELECT contrasena_P,correo_P,codigo_perteneciente FROM propietario WHERE correo_P='{email}'"
    cursor.execute(sql_propietario)
    resultado_propietario = cursor.fetchone()

    
    if resultado_usuario and contrasena == resultado_usuario[0]:
        session["logueado"] = True
        session["usuario_id"] = email
        session["usuario_nombre"] = resultado_usuario[1]
        return redirect(url_for('principal_cliente')) 
    elif resultado_barbero and contrasena == resultado_barbero[0]:
        session["logueado"] = True
        session["usuario_id"] = email
        session["usuario_nombre"] = resultado_barbero[1]
        return redirect(url_for('principal_barbero')) 
    elif resultado_propietario and contrasena == resultado_propietario[0]:
        session["logueado"] = True
        session["usuario_id"] = email
        session["usuario_nombre"] = resultado_propietario[1]
        sent = f"SELECT bnombre, apellido, fk_cedulaB FROM barberos WHERE codigo_perteneciente ='{resultado_propietario[2]}'"
        cursor.execute(sent)
        resultados = cursor.fetchall()
        return render_template('htmls_principal_page/principal_propietario.html', barberos=resultados)

    return render_template('login.html')
    
    
    

        #----//REGISTRO DE DATOS Y MANEJO DE ROLES EN EL REGISTRO-------//;
        #//------SE LLEVARA UNA SOLA INTERFAZ DE REGISTRO PARA EL USUARIO-------- //#
        #FUNCIONES DE LOGIN RESTAURAR ; LOGIN ; REGISTRAR CLIENTE#

@app.route("/registro", methods=['GET','POST'])
def registro():
    if request.method == 'POST':
        fk_cedula = request.form['cedula_registro']
        correo = request.form['correo_usuario']
        nombre = request.form['nombre_usuario']
        apellidos = request.form['apellidos_usuario']
        celular = request.form['celular_usuario']
        ciudad = request.form['ciudad_usuario']
        departamento = request.form['departamento']
        f_nacimiento = request.form['f_nacimiento_U']
        correo = request.form['correo_usuario']
        contrasena = request.form['contrasena']
    
        # Consultas SQL para verificar si la cédula ya existe en la tabla de usuarios
        sqlU_ced_existe = f"SELECT fk_cedulaU FROM usuario WHERE fk_cedulaU = %s"
        sqlU_ced_existe = f"SELECT pk_cedulaP FROM propietario WHERE fk_cedulaP = %s"
        sqlU_ced_existe = f"SELECT fk_cedulaB FROM barberos WHERE fk_cedulaB = %s"
        
        
        # Consultas SQL para verificar si el correo ya existe en las tablas
        sqlU_correo_existeu = f"SELECT correo FROM usuario WHERE correo = %s"
        sqlB_correo_existeb = f"SELECT bcorreo FROM barberos WHERE bcorreo = %s"
        sqlP_correo_existeP = f"SELECT correo_P FROM propietario WHERE correo_P = %s"
        
        conn = mysql.connect()
        cursor = conn.cursor()
        conn.commit()
        # Verificar si la cédula ya existe en la tabla de usuarios
        cursor.execute(sqlU_ced_existe, (fk_cedula,))
        usuario_existe = cursor.fetchone()
        
        # Verificar si el correo ya existe en la tabla de usuarios
        cursor.execute(sqlU_correo_existeu, (correo,))
        usuario_correo_existe = cursor.fetchone()
        
        # Verificar si el correo ya existe en la tabla de barberos
        cursor.execute(sqlB_correo_existeb, (correo,))
        barbero_correo_existe = cursor.fetchone()
        
        # Verificar si el correo ya existe en la tabla de propietarios
        cursor.execute(sqlP_correo_existeP, (correo,))
        propietario_correo_existe = cursor.fetchone()
        
       
        if usuario_existe:
            msj_error = "La cédula ya esta registrada. por favor Introduce una cédula valida"
            return render_template('/registro-1.html', msj=msj_error)
        
        elif usuario_correo_existe or barbero_correo_existe or propietario_correo_existe:
            msj_error_correo = "El correo  ya esta registrado. por favor ingresa un correo nuevo"
            return render_template('/registro-1.html', msj_C=msj_error_correo)
        
 
        fecha_nacimiento = datetime.strptime(request.form['f_nacimiento_U'], '%Y-%m-%d')
        fecha_actual = datetime.now()
        edad_calc = fecha_actual.year - fecha_nacimiento.year - ((fecha_actual.month, fecha_actual.day) < (fecha_nacimiento.month, fecha_actual.day))
        
        if edad_calc >= 18:
          
            t_sql = "INSERT INTO usuario (nombre, apellidos, celular, ciudad, f_nacimiento, correo, contrasena, rol, fk_cedulaU, departamento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s,%s)"
            cursor.execute(t_sql, (nombre, apellidos, celular, ciudad, f_nacimiento, correo, contrasena, 'cliente', fk_cedula, departamento))
            conn.commit()
            return redirect(url_for('principal_cliente')) 
        else:
            mensaje_edad = "No te puedes registrar porque no eres mayor de 18 años"
            return render_template('registro-1.html', msjedad=mensaje_edad)
        


    elif request.method == 'GET':
        return render_template('/registro-1.html')

    

        
        #RECUPERAR CONTRASEÑAAAA


@app.route("/recuperar_contra", methods=['GET', 'POST'])
def actualizar_contrasena():
    if request.method == 'POST':
        cedula = request.form['cedula_user']
        f_nacimiento = request.form['nacimiento_user']
        f_nacimiento = datetime.strptime(f_nacimiento, '%Y-%m-%d').date()
        nueva_contra = request.form['nueva_contra']

        conn = mysql.connect()
        cursor = conn.cursor()

        # Verificar en la tabla de usuarios
        sql_verificar_cliente = "SELECT fk_cedulaU FROM usuario WHERE fk_cedulaU = %s AND f_nacimiento = %s"
        cursor.execute(sql_verificar_cliente, (cedula, f_nacimiento))
        resultado_cliente = cursor.fetchone()

        # Verificar en la tabla de barberos
        sql_verificar_barbero = "SELECT fk_cedulaB FROM barberos WHERE fk_cedulaB = %s AND bf_nacimiento = %s"
        cursor.execute(sql_verificar_barbero, (cedula, f_nacimiento))
        resultado_barbero = cursor.fetchone()

        # Verificar en la tabla de propietarios
        sql_verificar_propietario = "SELECT pk_cedulaP FROM propietario WHERE pk_cedulaP = %s AND Pf_nacimiento = %s"
        cursor.execute(sql_verificar_propietario, (cedula, f_nacimiento))
        resultado_propietario = cursor.fetchone()

        if resultado_cliente:
            sql_actualizacion_cliente = "UPDATE usuario SET contrasena = %s WHERE fk_cedulaU = %s"
            cursor.execute(sql_actualizacion_cliente, (nueva_contra, cedula))
            conn.commit()
            exitoso = "Tu contraseña ha sido actualizada con éxito."
            return render_template('login.html', exito=exitoso)
        elif resultado_barbero:
            sql_actualizacion_barbero = "UPDATE barberos SET bcontrasena = %s WHERE fk_cedulaB = %s"
            cursor.execute(sql_actualizacion_barbero, (nueva_contra, cedula))
            conn.commit()
            exitoso = "Tu contraseña ha sido actualizada con éxito."
            return render_template('login.html', exito=exitoso)
        elif resultado_propietario:
            sql_actualizacion_propietario = "UPDATE propietario SET contrasena_P = %s WHERE pk_cedulaP = %s"
            cursor.execute(sql_actualizacion_propietario, (nueva_contra, cedula))
            conn.commit()
            exitoso = "Tu contraseña ha sido actualizada con éxito."
            return render_template('login.html', exito=exitoso)
        else:
            datos = "La información proporcionada es incorrecta. Por favor, inténtalo de nuevo."
            return render_template('recuperar_contra.html', invalidados=datos)
    
    return render_template('recuperar_contra.html')


    #__________________________________PERFILES_________________________________________________________#


            #________________________________CLIENTE____________________________#
@app.route('/perfil_usuario')
def perfil_usuario():
    if not session.get("logueado"):
        return render_template('login.html')

    email = session.get("usuario_id")
    conn = mysql.connect()
    cursor = conn.cursor()

    # OBTENGO LOS DATOS DEL CLIENTE PARA MOSTRARLOS EN PANTALLA
    sql_usuario = f"SELECT * FROM usuario WHERE correo='{email}'"

    cursor.execute(sql_usuario)
    #ALMACENO DICHOS DATOS PARA MANEJARLOS
    datos_usuario = cursor.fetchone()

    conn.commit()
    #SI LOS DATOS LLAMADOS ESTAN RENDERIZAR A EL PERFIL YA CON LOS DATOS OBTENIDOS DESDE EL JINJA CON LAS POSICIONES
    #DE LOS CAMPOS EN LA BASE DE DATOS 
    if datos_usuario:
        return render_template('perfiles/cliente.html', datos_usuario=datos_usuario)
    else:
        return "Usuario no encontrado", 404
    
@app.route('/subir_foto_cliente', methods=['POST'])
def subir_foto_cliente():
    if 'foto_perfil' not in request.files:
        return 'No se seleccionó ninguna imagen', 400

    file = request.files['foto_perfil']
    if file.filename == '':
        return 'No se seleccionó ninguna imagen', 400

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    email = session.get("usuario_id")  # Obtener el correo electrónico del cliente desde la sesión
    conn = mysql.connect()
    cursor = conn.cursor()

    sql_update = f"UPDATE usuario SET foto_u = '{filename}' WHERE correo='{email}'"
    cursor.execute(sql_update)
    conn.commit()

    return redirect(url_for('cargar_foto_cliente'))  # Redireccionar al perfil del cliente después de subir la foto

@app.route('/cargar_foto_cliente')
def cargar_foto_cliente():
    email = session.get("usuario_id")
    conn = mysql.connect()
    cursor = conn.cursor()

    sql_usuario = f"SELECT * FROM usuario WHERE correo='{email}'"
    cursor.execute(sql_usuario)
    datos_usuario = cursor.fetchone()

    conn.commit()

    if datos_usuario:
        # Renderiza la plantilla con la foto de perfil actualizada
        return render_template('perfiles/cliente.html', datos_usuario=datos_usuario)
    else:
        return "Usuario no encontrado", 404




 #__________________________________________________BARBERO______________________________________#

@app.route('/perfil_barbero') 
def perfil_barbero():
    if not session.get("logueado"):
        return render_template('login.html')

    email = session.get("usuario_id")
    conn = mysql.connect()
    cursor = conn.cursor()

    sql_barbero = f"SELECT * FROM barberos WHERE bcorreo='{email}'"

    cursor.execute(sql_barbero)
    datos_barbero = cursor.fetchone()

    conn.commit()

    if datos_barbero:
        return render_template('perfiles/perfil_barbero.html', datos_barbero=datos_barbero)
    else:
        return "Barbero no encontrado", 404

@app.route('/subir_foto_barbero', methods=['POST'])
def subir_foto_barbero():
    if 'foto_perfil' not in request.files:
        return 'No se seleccionó ninguna imagen', 400

    file = request.files['foto_perfil']
    if file.filename == '':
        return 'No se seleccionó ninguna imagen', 400

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    email = session.get("usuario_id")  
    conn = mysql.connect()
    cursor = conn.cursor()

    sql_update = f"UPDATE barberos SET foto_barbero = '{filename}' WHERE bcorreo='{email}'"
    cursor.execute(sql_update)
    conn.commit()

    return redirect(url_for('cargar_foto_barbero'))  

@app.route('/cargar_foto_barbero')
def cargar_foto_barbero():
    email = session.get("usuario_id")
    conn = mysql.connect()
    cursor = conn.cursor()

    sql_barbero = f"SELECT * FROM barberos WHERE bcorreo='{email}'"
    cursor.execute(sql_barbero)
    datos_barbero = cursor.fetchone()

    conn.commit()

    if datos_barbero:
        return render_template('perfiles/perfil_barbero.html', datos_barbero=datos_barbero)
    else:
        return "Barbero no encontrado", 404

@app.route('/principal_cliente', methods=['GET'])
def principal_cliente():
    conn = mysql.connect()
    cursor = conn.cursor()

   
    sql_barberias = "SELECT nom_barberia FROM barberia"
    cursor.execute(sql_barberias)
    barberias = cursor.fetchall()

    conn.commit()
    conn.close()

    
    return render_template('htmls_principal_page/principal_cliente.html', barberias=barberias)



@app.route('/principal_barbero', methods=['GET'])
def principal_barbero():
   
    if not session.get("logueado"):
        return render_template('login.html')

  
    email_barbero = session.get("usuario_id")
    if not email_barbero:
        return "El correo electrónico del barbero no está disponible en la sesión.", 404

   
    conn = mysql.connect()
    cursor = conn.cursor()

    
    sql_cedula_barbero = "SELECT fk_cedulaB FROM barberos WHERE bcorreo = %s"
    cursor.execute(sql_cedula_barbero, (email_barbero,))
    cedula_barbero_db = cursor.fetchone()

    if not cedula_barbero_db:
        return "La cédula del barbero no se encontró en la base de datos.", 404

    cedula_barbero_db = cedula_barbero_db[0]

    
    fecha_seleccionada = request.args.get('fecha')
    if not fecha_seleccionada:
        
        return render_template('htmls_principal_page/principal_barbero.html', mensaje="Por favor, selecciona una fecha para ver las citas.")

    
    sql_citas = f"SELECT nombre_cliente, apellidos_cliente, hora, fecha, telefono_cliente FROM citas_agendadas WHERE ced_barbero = '{cedula_barbero_db}' AND fecha = '{fecha_seleccionada}'"
    cursor.execute(sql_citas)
    citas = cursor.fetchall()

    
    if not citas:
        mensaje = f"No hay citas pendientes para el día seleccionado: {fecha_seleccionada}."
    else:
        mensaje = "Citas Pendientes"

    
    cursor.close()
    conn.close()

    
    return render_template('htmls_principal_page/principal_barbero.html', citas=citas, mensaje=mensaje)



@app.route('/perfil_barberias/<codigo>', methods=['GET'])
def perfil_barberias(codigo):
    conn = mysql.connect()
    cursor = conn.cursor()

    
    sql_barberia = f"SELECT * FROM barberia WHERE nom_barberia = '{codigo}'"
    cursor.execute(sql_barberia)
    datos_barberia = cursor.fetchone()

    
    if datos_barberia:
        codigo_barberia = datos_barberia[0]
    else:
        return "Barbería no encontrada", 404

    
    sql_horarios = f"SELECT * FROM horario_disponible WHERE pk_id_horario = '{codigo_barberia}'"
    cursor.execute(sql_horarios)
    horarios = cursor.fetchall()

  
   
    
    sql_servicios = f"SELECT * FROM servicios WHERE codigo_servicio = '{codigo_barberia}'"
    cursor.execute(sql_servicios)
    servicios = cursor.fetchall()

    conn.commit()
    conn.close()

    
    return render_template('cliente/perfil_negocios.html', datos_barberia=datos_barberia, horarios=horarios,servicios=servicios)


    #_____________________________________________PROPIETARIO__________________________________#
@app.route('/perfil_propietario')
def perfil_propietario():
    if not session.get("logueado"):
        return render_template('login.html')

    email = session.get("usuario_id")
    conn = mysql.connect()
    cursor = conn.cursor()

    
    sql_propietario = f"SELECT * FROM propietario WHERE correo_P='{email}'"

    cursor.execute(sql_propietario)
    datos_propietario = cursor.fetchone()

    conn.commit()

    if datos_propietario:

        return render_template('perfiles/propi.html', datos_propietario=datos_propietario)
    else:
        return "Propietario no encontrado", 404
    

@app.route('/subir_foto_perfil', methods=['POST'])
def subir_foto_perfil():
    if 'foto_perfil' not in request.files:
        return 'No se seleccionó ninguna imagen', 400

    file = request.files['foto_perfil']
    if file.filename == '':
        return 'No se seleccionó ninguna imagen', 400

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    
    email = session.get("usuario_id")
    conn = mysql.connect()
    cursor = conn.cursor()

    sql_update = f"UPDATE propietario SET foto_perfil = '{filename}' WHERE correo_P = '{email}'"
    cursor.execute(sql_update)
    conn.commit()

    return redirect(url_for('cargar_foto'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/cargar_foto')
def cargar_foto():
    email = session.get("usuario_id")
    conn = mysql.connect()
    cursor = conn.cursor()

    sql_propietario = f"SELECT * FROM propietario WHERE correo_P='{email}'"
    cursor.execute(sql_propietario)
    datos_propietario = cursor.fetchone()

    conn.commit()

    if datos_propietario:
       
        return render_template('perfiles/propi.html', datos_propietario=datos_propietario)
    else:
        return "Propietario no encontrado", 404
    
    
    

@app.route('/principal_propietario', methods=['GET'])
def principal_propietario():
    
    
    email_propietario = session.get("usuario_id")
    conn = mysql.connect()
    cursor = conn.cursor()

    sql_codigoP = f"SELECT codigo_perteneciente FROM propietario WHERE correo_P = '{email_propietario}'"
    cursor.execute(sql_codigoP)
    codigoP = cursor.fetchone() 

    if codigoP:
        codigoP = codigoP[0]

        sql_barberoB = f"SELECT   bnombre, apellido, fk_cedulaB FROM barberos WHERE codigo_perteneciente ='{codigoP}' "
        cursor.execute(sql_barberoB)
        barberos = cursor.fetchall()

        conn.commit()
        conn.close()
      
        return render_template('htmls_principal_page/principal_propietario.html', barberos=barberos)

    conn.close()


    #ELIMINACION DE BAREBROS POR PARTE DEL PROPIETARIO 
    
@app.route('/eliminar_barbero/<ced>')
def eliminar_barbero(ced):
    

    eliminar_barbero = f"DELETE FROM barberos WHERE fk_cedulaB = '{ced}'"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(eliminar_barbero)
    conn.commit()

    return redirect('/cargar_barberos')
    #return render_template('/htmls_principal_page/principal_propietario.html' )

#ACTUALIZAR DATOS

@app.route('/cargar_barberos')
def cargar_barberos():

    email_propietario = session.get("usuario_id")
    conn = mysql.connect()
    cursor = conn.cursor()
    sql_codigoP = f"SELECT codigo_perteneciente FROM propietario WHERE correo_P = '{email_propietario}'"
    cursor.execute(sql_codigoP)
    codigoP = cursor.fetchone()

    if codigoP:
        codigoP = codigoP[0]
    
        sql_barberoB = f"SELECT bnombre, apellido, fk_cedulaB FROM barberos WHERE codigo_perteneciente ='{codigoP}' "
        cursor.execute(sql_barberoB)
        barberos_actualizados = cursor.fetchall()

        conn.commit()
        conn.close()

        
        return render_template('htmls_principal_page/principal_propietario.html', barberos=barberos_actualizados)
    else:
        
        return "Propietario no encontrado", 404
    



@app.route('/Registro_barbero', methods=['GET','POST'])
def registrar_barbero():
    if not session.get("logueado"):
        return render_template('login.html')
    if request.method == 'POST':
        cedula_barbero = request.form['cedula_barberoP']
        Nombre_barbero = request.form['nombre_barberoP']
        Apellidos_barbero = request.form['apellidos_barberoP']
        correo_barbero = request.form['correo_barberoP']
        celular_barbero = request.form['celular_barberoP']
        ciudad_barbero = request.form['ciudad_barberoP']
        f_nacimiento_barbero = request.form['f_nacimiento_bP']
        contrasena = request.form['contrasena_barberoP']
        confir_contrasenabP = request.form['confir_contra_barberoP']
        bdepartamento = request.form['departamento_barberoP']

        conn = mysql.connect()
        cursor = conn.cursor()

        correo_propietario = session.get("usuario_id")
        if not correo_propietario:
            return "No se encontró el propietario en sesión", 401

        cursor.execute("SELECT pk_cedulaP, nombre_P, codigo_barberia FROM propietario WHERE correo_P = %s", (correo_propietario,))
        propietario_info = cursor.fetchone()

        if propietario_info:
            cedula_propietario = propietario_info[0]
            codigo_barberia_propietario = propietario_info[2]

            cursor.execute("SELECT * FROM barberos WHERE fk_cedulaB = %s", (cedula_barbero,))
            barbero_existe = cursor.fetchone()

            if barbero_existe:
                return render_template('registro_barbero.html', msj="El trabajador ya está registrado con este documento. Por favor ingresa uno nuevo")

            cursor.execute("SELECT pk_cedulaP FROM propietario WHERE pk_cedulaP = %s", (cedula_barbero,))
            propietario_existe = cursor.fetchone()

            if propietario_existe:
                return render_template('registro_barbero.html', msj_error_propietario="La cédula ya está registrada como propietario. Por favor ingresa una cédula diferente.")

            cursor.execute("SELECT fk_cedulaU FROM usuario WHERE fk_cedulaU = %s", (cedula_barbero,))
            usuario_existe = cursor.fetchone()

            if usuario_existe:
                return render_template('registro_barbero.html', msj_error_cliente="La cédula ya está registrada como cliente. Por favor ingresa una cédula diferente.")

            cursor.execute("SELECT fk_cedulaB FROM barberos WHERE fk_cedulaB = %s", (cedula_barbero,))
            barbero_existe_cedula = cursor.fetchone()

            if barbero_existe_cedula:
                return render_template('registro_barbero.html', msjB="El trabajador ya está registrado con este documento. Por favor ingresa uno nuevo")

            cursor.execute("SELECT bcorreo FROM barberos WHERE bcorreo = %s", (correo_barbero,))
            correo_existente = cursor.fetchone()

            cursor.execute("SELECT correo FROM usuario WHERE correo = %s", (correo_barbero,))
            correo_existente_U = cursor.fetchone()

            cursor.execute("SELECT correo_P FROM propietario WHERE correo_P = %s", (correo_barbero,))
            correo_existente_P = cursor.fetchone()

            if correo_existente or correo_existente_U or correo_existente_P:
                return render_template('registro_barbero.html', error_correo="El correo ya está registrado. Ingresa uno nuevo.")

            fecha_nacimiento = datetime.strptime(f_nacimiento_barbero, '%Y-%m-%d')
            fecha_actual = datetime.now()
            edad_calc = fecha_actual.year - fecha_nacimiento.year - ((fecha_actual.month, fecha_actual.day) < (fecha_actual.month, fecha_actual.day))

            if contrasena == confir_contrasenabP and edad_calc >= 18:
                codigo_perteneciente = f"{cedula_propietario}"
                sql_insert = "INSERT INTO barberos (fk_cedulaB, bnombre, apellido, bcorreo, bcelular, bciudad, bf_nacimiento, bcontrasena, rol, codigo_perteneciente, bdepartamento, fk_codigo_barberia) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql_insert, (cedula_barbero, Nombre_barbero, Apellidos_barbero, correo_barbero, celular_barbero, ciudad_barbero, f_nacimiento_barbero, contrasena, "barbero", codigo_perteneciente, bdepartamento, codigo_barberia_propietario))

                cursor.execute("UPDATE propietario SET codigo_perteneciente = %s WHERE pk_cedulaP = %s", (codigo_perteneciente, cedula_propietario))

                conn.commit()

                return render_template('registro_barbero.html')
            else:
                return render_template('registro_barbero.html', mensaje_edad="El barbero necesita ser mayor de edad para registrarse.")
        else:
            return render_template('registro_barbero.html', mensaje_error="No se pudo obtener la información del propietario.")
    else:
        return render_template('registro_barbero.html')





#<------------ EDICION DE PERFILES CLIENTE, BARBERO, PROPIETARIO  -------------------------->
@app.route('/editar_user', methods=['GET', 'POST'])
def editar_user():
    if not session.get("logueado"):
        return redirect('/login')

    if request.method == 'POST':
        edit_cedula = request.form['ced_U']
        edit_celular = request.form['Tel_U']
        edit_ciudad = request.form['ciudad_U']

        conn = mysql.connect()
        cursor = conn.cursor()
        
        # Consulta SQL para actualizar los datos del usuario
        sql_act_U = f"UPDATE usuario SET celular='{edit_celular}', ciudad='{edit_ciudad}'  WHERE fk_cedulaU='{edit_cedula}'"
        
        cursor.execute(sql_act_U)
        conn.commit()

        
        email_usuario = session.get("usuario_id")
        sql_usuario = f"SELECT * FROM usuario WHERE correo='{email_usuario}'"
        cursor.execute(sql_usuario)
        datos_usuario = cursor.fetchone()
        conn.commit()

        return render_template('perfiles/cliente.html', datos_usuario=datos_usuario)
    else:
        email_usuario = session.get("usuario_id")
        conn = mysql.connect()
        cursor = conn.cursor()
        sql_usuario = f"SELECT * FROM usuario WHERE correo='{email_usuario}'"
        cursor.execute(sql_usuario)
        datos_usuario = cursor.fetchone()
        conn.commit()

        if datos_usuario:
            return render_template('Actualizacion_perfiles/editar_cliente.html', datos_usuario=datos_usuario)
        else:
            return "Usuario no encontrado", 404



@app.route('/editar_barbero', methods=['GET', 'POST'])
def editar_barbero():
    if not session.get("logueado"):
        return redirect('/login')

    if request.method == 'POST':
        edit_cedula = request.form['ced_B']
        edit_celular = request.form['Tel_B']
        edit_ciudad = request.form['ciudad_B']

        conn = mysql.connect()
        cursor = conn.cursor()
        
        
        sql_act_B = f"UPDATE barberos SET  bcelular='{edit_celular}', bciudad='{edit_ciudad}' WHERE fk_cedulaB='{edit_cedula}'"
        
        cursor.execute(sql_act_B)
        conn.commit()

        return redirect('/perfil_barbero')
    else:
        email_barbero = session.get("usuario_id")
        conn = mysql.connect()
        cursor = conn.cursor()
        select_b = f"SELECT * FROM barberos WHERE bcorreo='{email_barbero}'"
        cursor.execute(select_b)
        datos_barbero = cursor.fetchone()
        conn.commit()

        if datos_barbero:
            return render_template('Actualizacion_perfiles/editar_perfil_barberos.html', datos_barbero=datos_barbero)
        else:
            return "Usuario no encontrado", 404



@app.route('/editar_propietario', methods=['GET', 'POST'])
def editar_propietario():
    if not session.get("logueado"):
        return redirect('/login')

    if request.method == 'POST':
        edit_cedula = request.form['ced_P']
        edit_celular = request.form['Celular_P']
        edit_ciudad = request.form['Ciudad_P']

        conn = mysql.connect()
        cursor = conn.cursor()
        
        
        sql_act_P = f"UPDATE propietario SET  celular_P='{edit_celular}', Pciudad='{edit_ciudad}' WHERE pk_cedulaP='{edit_cedula}'"
        
        cursor.execute(sql_act_P)
        conn.commit()

        
        email_propietario = session.get("usuario_id")
        select_p = f"SELECT * FROM propietario WHERE correo_P='{email_propietario}'"
        cursor.execute(select_p)
        datos_propietario = cursor.fetchone()

        return render_template('perfiles/propi.html', datos_propietario=datos_propietario)
    else:
        email_propietario = session.get("usuario_id")
        conn = mysql.connect()
        cursor = conn.cursor()
        select_p = f"SELECT * FROM propietario WHERE correo_P='{email_propietario}'"
        cursor.execute(select_p)
        datos_propietario = cursor.fetchone()

        if datos_propietario:
            return render_template('Actualizacion_perfiles/editar_perfil_propietario.html', datos_propietario=datos_propietario)
        else:
            return "Usuario no encontrado", 404



                                        #BARBERIA


#----------------------------------BARBERIA REGISTRO--------------------_----#
@app.route('/barberia_registro', methods=['GET', 'POST'])
def barberia_registro():
    if request.method == 'POST':
        nombre_barberia = request.form['nombre_barberia']
        direccion_barberia = request.form['direccion_barberia']
        ciudad_negocio = request.form['ciudad_negocio']
        telefono_negocio = request.form['telefono_negocio']
        pais_negocio = request.form['Pais_negocio']
        departamento_negocio = request.form['departamento_negocio']
        hora_apertura = request.form['hora_A']
        hora_cierre = request.form['hora_C']

        
        correo_propietario = session.get('usuario_id')
        if not correo_propietario:
            return "El propietario no está registrado.", 404

        
        codigo_unico = f"{nombre_barberia}-{ciudad_negocio}-{telefono_negocio}"

        
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM barberia WHERE pk_codigo_barberia = '{codigo_unico}'")
        existencia = cursor.fetchone()

        
        cursor.execute(f"SELECT * FROM barberia WHERE correo = '{correo_propietario}'")
        barberia_existente = cursor.fetchone()

        if existencia or barberia_existente:
            mensaje = "Ya tienes una barbería registrada."
            return render_template('barberia/barberiaR.html', mensaje=mensaje)
        else:
          
            cursor.execute("INSERT INTO barberia (nom_barberia, direccion, ciudad, telefono, correo, pais, departamento, pk_codigo_barberia, h_apertura, h_cierre) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (nombre_barberia, direccion_barberia, ciudad_negocio, telefono_negocio, correo_propietario, pais_negocio, departamento_negocio, codigo_unico, hora_apertura, hora_cierre))

            
            cursor.execute(f"SELECT pk_cedulaP FROM propietario WHERE correo_P = '{correo_propietario}'")
            propietario_id = cursor.fetchone()

            if propietario_id:
                cursor.execute("UPDATE propietario SET nom_barberia = %s, codigo_barberia = %s WHERE pk_cedulaP = %s", (nombre_barberia, codigo_unico, propietario_id[0]))

                conn.commit()
                conn.close()

                mensaje = "La barbería se registró exitosamente."
                return redirect(url_for('cargar_barberos'))
            else:
                conn.close()
                return "El propietario no está registrado.", 404

    return render_template('barberia/barberiaR.html')



                            
                            #PERFIL BARBERIA 

@app.route('/perfil_barberia')
def perfil_barberia():
    if not session.get("logueado"):
        return render_template('login.html')

    email_propietario = session.get("usuario_id")
    conn = mysql.connect()
    cursor = conn.cursor()

   
    sql_barberia = f"SELECT * FROM barberia WHERE correo='{email_propietario}'"
    cursor.execute(sql_barberia)
    datos_barberia = cursor.fetchone()

    conn.commit()
    conn.close()

    if datos_barberia:
    
        return render_template('perfiles/perfil_barberia.html', datos_barberia=datos_barberia)
    else:
        return "Barbería no encontrada", 404



@app.route('/subir_foto_barberia', methods=['POST'])
def subir_foto_barberia():
    if 'foto_perfil' not in request.files:
        return 'No se seleccionó ninguna imagen', 400

    file = request.files['foto_perfil']
    if file.filename == '':
        return 'No se seleccionó ninguna imagen', 400

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    email = session.get("usuario_id")
    conn = mysql.connect()
    cursor = conn.cursor()

    sql_update = f"UPDATE barberia SET imagenb = '{filename}' WHERE correo='{email}'"
    cursor.execute(sql_update)
    conn.commit()

    return redirect(url_for('perfil_barberia'))



@app.route('/registrar_horarios', methods=['GET', 'POST'])
def registrar_horarios():
    if 'usuario_id' not in session:
        return "El propietario no está registrado.", 404

    correo_propietario = session['usuario_id']

    if request.method == 'POST':
        dia_inicio = request.form['dia_inicio']
        dia_fin = request.form['dia_fin']
        hora_inicio = request.form['hora_inicio']
        hora_fin = request.form['hora_fin']

        if hora_inicio >= hora_fin:
            return "La hora de inicio debe ser antes de la hora de fin.", 400

        conn = mysql.connect()
        cursor = conn.cursor()

        
        cursor.execute("SELECT codigo_barberia FROM propietario WHERE correo_P = %s", (correo_propietario,))
        codigo_barberia = cursor.fetchone()[0]

       
        cursor.execute("SELECT COUNT(*) FROM horario_disponible WHERE pk_id_horario = %s", (codigo_barberia,))
        count = cursor.fetchone()[0]

        if count > 0:
            
            mesange = "La barbería ya tiene horarios registrados. Contacta el administrador para actualizar los horarios."
            return render_template('barberia/registrar_horario.html', message=mesange), 400
        
        cursor.execute("INSERT INTO horario_disponible (pk_id_horario, dia_inicio, dia_fin, hora_inicio, hora_fin) VALUES (%s, %s, %s, %s, %s)",
                       (codigo_barberia, dia_inicio, dia_fin, hora_inicio, hora_fin))

        conn.commit()
        mens = "Horarios registrados exitosamente."
        return render_template('barberia/registrar_horario.html', meage=mens)

    return render_template('barberia/registrar_horario.html')







# lo de mostrar los horarios lo haremos con los clientes  

@app.route('/mostrar_horarios_barberia')
def horarios_barberia():
   
    if not session.get("logueado"):
        return render_template('login.html')

    email_propietario = session.get("usuario_id")
    conn = mysql.connect()
    cursor = conn.cursor()
    
    
    
    
    conn = mysql.connect()
    cursor = conn.cursor()
    

    cursor.execute("SELECT pk_cedulaP FROM propietario WHERE correo_P = %s", (email_propietario,))
    resultado = cursor.fetchone()
    
    if not resultado:
        return "No se encontró la cédula del propietario.", 404
    
    cedula_propietario = resultado[0]
    print(cedula_propietario)

    cursor.execute("SELECT * FROM horario_disponible WHERE pk_id_horario = %s", (cedula_propietario,))
    horarios = cursor.fetchall()
    

    cursor.close()
    conn.close()
    
    return render_template('barberia/mostrar_horario.html', horarios=horarios)


#REGISTRAR SERVICIOS

@app.route('/registrar_servicios', methods=['GET', 'POST'])
def registrar_servicios():
    if request.method == 'POST':
        nombre_servicio = request.form['nombre_servicio']
        precio_servicio = request.form['precio_servicio']

        
        correo_propietario = session.get('usuario_id')
        if not correo_propietario:
            return "El propietario no está registrado.", 404

        
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT pk_codigo_barberia FROM barberia WHERE correo = %s", (correo_propietario,))
        codigo_barberia = cursor.fetchone()

        if not codigo_barberia:
            return "La barbería no está registrada.", 404

        
        cursor.execute("INSERT INTO servicios (codigo_servicio, nombre, precio) VALUES (%s, %s, %s)",
                       (codigo_barberia[0], nombre_servicio, precio_servicio))

        conn.commit()
        conn.close()

        flash('Has guardado el servicio de manera exitosa. Si deseas agregar otro servicio, agregalo.')
        
        return redirect(url_for('registrar_servicios'))

    return render_template('barberia/registrar_servicios.html')


#CERRAR SESION 
@app.route('/cerrar_sesion', methods=['GET'])
def cerrar_sesion():
    session.clear() 
    return redirect(url_for('index')) 




@app.route('/barberos/<codigo_barberia>', methods=['GET'])
def mostrar_barberos(codigo_barberia):
    conn = mysql.connect()
    cursor = conn.cursor()

   
    cursor.execute("SELECT * FROM barberos WHERE fk_codigo_barberia = %s", (codigo_barberia,))
    barberos = cursor.fetchall()

    return render_template('cliente/barberos_disponibles.html', barberos=barberos)



@app.route('/perfil_barbero/<cedula_barbero>', methods=['GET'])
def perfilC_barbero(cedula_barbero):
    conn = mysql.connect()
    cursor = conn.cursor()

    
    cursor.execute("SELECT * FROM barberos WHERE fk_cedulaB = %s", (cedula_barbero,))
    barbero = cursor.fetchone()

    if barbero:
        return render_template('cliente/perfilCbarberos.html', barbero=barbero)
    else:
        return "Barbero no encontrado", 404




@app.route('/registrar_horarios_barbero', methods=['GET', 'POST'])
def registrar_horas():
    if 'usuario_id' not in session:
        return "El barbero no está registrado.", 404

    correo_barbero = session['usuario_id']

    if request.method == 'POST':
        conn = mysql.connect()
        cursor = conn.cursor()

        
        cursor.execute("SELECT fk_codigo_barberia, fk_cedulaB FROM barberos WHERE bcorreo = %s", (correo_barbero,))
        result = cursor.fetchone()
        if result is None:
            return "No se encontró la información del barbero.", 404
        codigo_barberia, cedula_b = result

        # Lista de días de la semana
        dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

       
        for fecha, dia_seleccionado, hora_inicio, hora_fin in zip(request.form.getlist('fecha[]'), request.form.getlist('dia_semana[]'), request.form.getlist('hora_inicio[]'), request.form.getlist('hora_fin[]')):
            
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')
            
            dia_semana = fecha_obj.weekday()
            
            indice_dia_seleccionado = dias_semana.index(dia_seleccionado)

            
            if dia_semana != indice_dia_seleccionado:
                return "El día seleccionado no coincide con la fecha.", 400

            if hora_inicio >= hora_fin:
                return "La hora de inicio debe ser antes de la hora de fin.", 400

            cursor.execute("INSERT INTO horario_cita_barbero (pk_idhorariob, hora_inicio, hora_fin, dia_semana, fecha, codigo_barberia, cedula_b) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           (codigo_barberia, hora_inicio, hora_fin, dia_seleccionado, fecha, codigo_barberia, cedula_b))

        conn.commit()

        return render_template('barbero/registrar_horas.html', message="Horarios registrados exitosamente.")

    return render_template('barbero/registrar_horas.html')




@app.route('/seleccionar_servicios/<cedula_barbero>', methods=['GET'])
def seleccionar_servicios(cedula_barbero):
    
    conn = mysql.connect()
    cursor = conn.cursor()

   
    cursor.execute("SELECT fk_codigo_barberia FROM barberos WHERE fk_cedulaB = %s", (cedula_barbero,))
    codigo_barberia = cursor.fetchone()[0]

   
    cursor.execute("SELECT * FROM servicios WHERE codigo_servicio = %s", (codigo_barberia,))
    servicios = cursor.fetchall()
    
    print("Servicios obtenidos:", servicios)

    
    cursor.close()
    conn.close()

    return render_template('cliente/seleccionar_servicios.html', servicios=servicios, cedula_barbero=cedula_barbero)

@app.route('/guardar_cita', methods=['GET','POST'])
def guardar_cita():
    if request.method == 'POST':
        cedula_barbero = request.form['cedula_barbero']
        servicios_seleccionados = request.form.getlist('servicios_seleccionados')
        fecha = request.form['fecha']
        hora = request.form['hora']
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        telefono = request.form['telefono']

        
        conn = mysql.connect()
        cursor = conn.cursor()

        
        cursor.execute("SELECT * FROM horario_cita_barbero WHERE fecha = %s AND hora_inicio = %s AND cedula_b = %s", (fecha, hora, cedula_barbero))
        horario_disponible = cursor.fetchone()

        if horario_disponible:
            
            for servicio_id in servicios_seleccionados:
                
                cursor.execute("SELECT nombre, precio FROM servicios WHERE codigo_servicio = %s", (servicio_id,))
                servicio = cursor.fetchone()
                if servicio:
                    nombre_servicio, precio_servicio = servicio
                    
                    cursor.execute("INSERT INTO citas_agendadas (ced_barbero, fk_codi_servicio, nombre_servicio, precio_servicio, fecha, hora, nombre_cliente, apellidos_cliente, telefono_cliente) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (cedula_barbero, servicio_id, nombre_servicio, precio_servicio, fecha, hora, nombre, apellidos, telefono))
                    
                    cursor.execute("UPDATE horario_cita_barbero SET disponible = 'Horario ocupado' WHERE codigo_barberia = %s", (servicio_id,))

          
            conn.commit()
            cursor.close()
            conn.close()

            return redirect(url_for('principal_cliente'))
        else:
            
            return "Lo sentimos, el horario seleccionado no está disponible. Por favor, elija otro horario."

@app.route("/mostrar_horarios_disponibles", methods=['GET', 'POST'])
def mostrar_horarios_disponibles():
    if request.method == 'POST':
        cedula_barbero = request.form['cedula_barbero']
        fecha = request.form['fecha']

        
        if not fecha:
            
            return render_template('horarios_disponible.html', cedula_barbero=cedula_barbero, horarios=None, error="Por favor, selecciona una fecha.")

        conn = mysql.connect()
        cursor = conn.cursor()

       
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()

        
        cursor.execute("SELECT hora_inicio, hora_fin, dia_semana, disponible FROM horario_cita_barbero WHERE fecha = %s AND cedula_b = %s", (fecha_obj, cedula_barbero))
        horarios = cursor.fetchall()

        print("Fecha enviada por el usuario:", fecha_obj)
        print("Cédula del barbero:", cedula_barbero)
        print("Horarios obtenidos:", horarios)

       
        cursor.close()
        conn.close()

        
        if not horarios:
            
            return render_template('horarios_disponible.html', cedula_barbero=cedula_barbero, horarios=None, error="No hay horarios disponibles este día, por favor selecciona otro .")

        
        return render_template('horarios_disponible.html', cedula_barbero=cedula_barbero, horarios=horarios)
    else:
        
        return render_template('horarios_disponible.html', cedula_barbero=request.args.get('cedula_barbero', ''), horarios=None)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port="5080")
