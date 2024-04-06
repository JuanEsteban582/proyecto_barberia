from conexion import *
from datetime import datetime


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
        return render_template('htmls_principal_page/principal_cliente.html')
    elif resultado_barbero and contrasena == resultado_barbero[0]:
        session["logueado"] = True
        session["usuario_id"] = email
        session["usuario_nombre"] = resultado_barbero[1]
        return render_template('htmls_principal_page/principal_barbero.html')
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

@app.route("/registro", methods=['GET','POST'])
def registro():
    if request.method == 'POST':
        fk_cedula = request.form['cedula_registro']
        correo = request.form['correo_usuario']
        nombre = request.form['nombre_usuario']
        apellidos = request.form['apellidos_usuario']
        celular = request.form['celular_usuario']
        ciudad = request.form['ciudad_Usuario']#
        departamento = request.form['departamento']
        f_nacimiento = request.form['f_nacimiento_U']
        correo = request.form['correo_usuario']
        contrasena = request.form['contrasena']
    
        # Consultas SQL para verificar si la cédula ya existe en la tabla de usuarios
        sqlU_ced_existe = f"SELECT fk_cedulaU FROM usuario WHERE fk_cedulaU = %s"
        
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
        
        # Si la cédula o el correo ya existen, mostrar un mensaje de error
        if usuario_existe:
            msj_error = "La cédula ya esta registrada. por favor Introduce una cédula valida"
            return render_template('/registro-1.html', msj=msj_error)
        
        elif usuario_correo_existe or barbero_correo_existe or propietario_correo_existe:
            msj_error_correo = "El correo  ya esta registrado. por favor ingresa un correo nuevo"
            return render_template('/registro-1.html', msj_C=msj_error_correo)
        
        # Aquí continúa tu lógica de registro para clientes...
        # Calcular la edad y verificar si el usuario es mayor de edad
        fecha_nacimiento = datetime.strptime(request.form['f_nacimiento_U'], '%Y-%m-%d')
        fecha_actual = datetime.now()
        edad_calc = fecha_actual.year - fecha_nacimiento.year - ((fecha_actual.month, fecha_actual.day) < (fecha_nacimiento.month, fecha_actual.day))
        
        if edad_calc >= 18:
            # Realizar el registro en la tabla de CLIENTES
            t_sql = "INSERT INTO usuario (nombre, apellidos, celular, ciudad, f_nacimiento, correo, contrasena, rol, fk_cedulaU, departamento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s,%s)"
            cursor.execute(t_sql, (nombre, apellidos, celular, ciudad, f_nacimiento, correo, contrasena, 'cliente', fk_cedula, departamento))
            conn.commit()
            return render_template('htmls_principal_page/principal_cliente.html')
        else:
            mensaje_edad = "No te puedes registrar porque no eres mayor de 18 años"
            return render_template('registro-1.html', msjedad=mensaje_edad)
        


    elif request.method == 'GET':
        return render_template('/registro-1.html')

    

        
        


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

                        #<<<<<<<<<<<<<<<<<<<<PERFILESSS>>>>>>>>>>>>>>>>>>>>>>>>>>#


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
        return render_template('perfiles/perfil_usuario.html', datos_usuario=datos_usuario)
    else:
        return "Usuario no encontrado", 404


#LO MISMO QUE PERFIL CLIENTE
@app.route('/perfil_barbero') 
def perfil_barbero():
    if not session.get("logueado"):
        return render_template('login.html')
    #EMAIL DEL USUARIO QUE  ESTA DENTRO DE LA SESION 
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
        # Renderiza la plantilla con la foto de perfil actualizada
        return render_template('perfiles/propi.html', datos_propietario=datos_propietario)
    else:
        return "Propietario no encontrado", 404


    
""" 
@app.route('/perfil_barberia')
def perfil_barberia():   
    
    email = session.get("usuario_id")
    conn = mysql.connect()
    cursor = conn.cursor()


    sql_barberia = f"SELECT * FROM barberia WHERE correo_P='{email}'"
 """
            #------------------------PAGINAS PRINCIPALES-----------------------------#


@app.route('/principal_cliente')
def principal_cliente():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM barberia")
    barberias = cursor.fetchall()  

    
    conn.close()


    return render_template('htmls_principal_page/principal.html_cliente', barberias=barberias)


@app.route('/principal_propietario', methods=['GET'])
def principal_propietario():
    
    
    email_propietario = session.get("usuario_id")
    conn = mysql.connect()
    cursor = conn.cursor()

    sql_codigoP = f"SELECT codigo_perteneciente FROM propietario WHERE correo_P = '{email_propietario}'"
    cursor.execute(sql_codigoP)
    codigoP = cursor.fetchone() # Aquí obtenemos el resultado de la consulta

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

        # Renderizar la plantilla 'principal_propietario.html' con los datos actualizados de los barberos
        return render_template('htmls_principal_page/principal_propietario.html', barberos=barberos_actualizados)
    else:
        # Manejar el caso en que no se encuentre el propietario
        return "Propietario no encontrado", 404


@app.route('/principal_barbero')
def principal_barbero():
    return render_template('htmls_principal_page/principal_barbero.html')




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
        sql_act_U = f"UPDATE usuario SET   celular='{edit_celular}', ciudad='{edit_ciudad}'  WHERE fk_cedulaU='{edit_cedula}'"
        
        cursor.execute(sql_act_U)
        conn.commit()

        return redirect('/perfil_usuario')
    else:
        email_usuario = session.get("usuario_id")
        conn = mysql.connect()
        cursor = conn.cursor()
        sql_usuario = f"SELECT * FROM usuario WHERE correo='{email_usuario}'"
        cursor.execute(sql_usuario)
        datos_usuario = cursor.fetchone()
        conn.commit()

        if datos_usuario:
            return render_template('Actualizacion_perfiles/editar_perfil_usuario.html', datos_usuario=datos_usuario)
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
        
        # Consulta SQL para actualizar los datos del usuario
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
            return render_template('Actualizacion_perfiles/editar_perfil_barbero.html', datos_barbero=datos_barbero)
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
        
        # Consulta SQL para actualizar los datos del usuario
        sql_act_P = f"UPDATE propietario SET  celular_P='{edit_celular}', Pciudad='{edit_ciudad}' WHERE pk_cedulaP='{edit_cedula}'"
        
        cursor.execute(sql_act_P)
        conn.commit()

        # Ahora obtenemos nuevamente los datos actualizados del propietario
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




@app.route('/Registro_barbero', methods=['GET','POST'])
def registrar_barbero():
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

        cursor.execute("SELECT * FROM barberos WHERE fk_cedulaB = %s", (cedula_barbero,))
        barbero_existe = cursor.fetchone()

        # Calcular edad
        fecha_nacimiento = datetime.strptime(f_nacimiento_barbero, '%Y-%m-%d')
        fecha_actual = datetime.now()
        edad_calc = fecha_actual.year - fecha_nacimiento.year - ((fecha_actual.month, fecha_actual.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

        if barbero_existe:
            msj_error = "El trabajador ya está registrado con este documento. Por favor ingresa uno nuevo"
            return render_template('registro_barbero.html', msj=msj_error)

       
        cursor.execute("SELECT * FROM barberos WHERE bcorreo = %s", (correo_barbero,))
        correo_existente = cursor.fetchone()
        if correo_existente:
            error_correo = "El correo ya está registrado. Ingresa uno nuevo."
            return render_template('registro_barbero.html', error_correo=error_correo)

        if contrasena == confir_contrasenabP:
            if edad_calc >= 18:
            
                cursor.execute("SELECT pk_cedulaP, nombre_P FROM propietario")
                propietario_info = cursor.fetchone()
            if propietario_info:
                cedula_propietario = propietario_info[0]
                
        
        # GENERACION DE CODIGO PERTENECIENTE
                codigo_perteneciente = f"{cedula_propietario}"
        
        
                sql_insert = "INSERT INTO barberos (fk_cedulaB, bnombre, apellido, bcorreo, bcelular, bciudad, bf_nacimiento, bcontrasena, rol, codigo_perteneciente, bdepartamento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)"
                cursor.execute(sql_insert, (cedula_barbero, Nombre_barbero, Apellidos_barbero, correo_barbero, celular_barbero, ciudad_barbero, f_nacimiento_barbero, contrasena,"barbero", codigo_perteneciente, bdepartamento ))
     
                cursor.execute("UPDATE propietario SET codigo_perteneciente = %s WHERE pk_cedulaP = %s", (codigo_perteneciente, cedula_propietario))
        
                conn.commit()

                mensaje_exito = "El barbero ha sido registrado con éxito."
                return render_template('registro_barbero.html', mensaje_exito=mensaje_exito)
        else:
            mensaje_error = "No se pudo obtener la información del propietario."
        return render_template('registro_barbero.html', mensaje_error=mensaje_error)
    else:
        mensaje_edad = "El barbero necesita ser mayor de edad para registrarse."
    return render_template('registro_barbero.html', mensaje_edad=mensaje_edad)



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

        # Recuperar el correo electrónico del propietario de la sesión
        correo_propietario = session.get('usuario_id')
        if not correo_propietario:
            return "El propietario no está registrado.", 404

        # Crear el código único
        codigo_unico = f"{nombre_barberia}-{ciudad_negocio}-{telefono_negocio}"

        # Verificar si el código único ya existe en la tabla barberias
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM barberia WHERE pk_codigo_barberia = '{codigo_unico}'")
        existencia = cursor.fetchone()

        if existencia:
            mensaje = "La barbería ya está registrada."
            return render_template('barberia/barberiaR.html', mensaje=mensaje)
        else:
            # Registrar la barbería con el código único en la tabla barberias
            cursor.execute("INSERT INTO barberia (nom_barberia, direccion, ciudad, telefono, correo, pais, departamento, pk_codigo_barberia, h_apertura, h_cierre) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (nombre_barberia, direccion_barberia, ciudad_negocio, telefono_negocio, correo_propietario, pais_negocio, departamento_negocio, codigo_unico, hora_apertura, hora_cierre))

            # Obtener el ID del propietario
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



@app.route('/registrar_horarios', methods=['GET','POST'])
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
        cursor.execute("SELECT pk_cedulaP FROM propietario WHERE correo_P = %s", (correo_propietario,))
        resultado = cursor.fetchone()
        
        if not resultado:
            return "No se encontró la cédula del propietario.", 404
        
        cedula_propietario = resultado[0]
        
        # Verifica si ya existen horarios registrados para el propietario
        cursor.execute("SELECT COUNT(*) FROM horario_disponible WHERE pk_id_horario = %s", (cedula_propietario,))
        count = cursor.fetchone()[0]
        
        if count > 0:
            # Si ya existen horarios, muestra un mensaje al usuario
            return "La barbería ya tiene horarios registrados. Ve al perfil de la barbería y actualízalos.", 400
        
        # Si no existen horarios, procede con la inserción
        cursor.execute("INSERT INTO horario_disponible (pk_id_horario, dia_inicio, dia_fin, hora_inicio, hora_fin) VALUES (%s, %s, %s, %s, %s)",
                       (cedula_propietario, dia_inicio, dia_fin, hora_inicio, hora_fin))
        
        conn.commit()
        
        return render_template('barberia/registrar_horario.html', message="Horarios registrados exitosamente.")
    
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

        # Recuperar el correo electrónico del propietario de la sesión
        correo_propietario = session.get('usuario_id')
        if not correo_propietario:
            return "El propietario no está registrado.", 404

        # Obtener el código único de la barbería del propietario
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT pk_codigo_barberia FROM barberia WHERE correo = %s", (correo_propietario,))
        codigo_barberia = cursor.fetchone()

        if not codigo_barberia:
            return "La barbería no está registrada.", 404

        # Insertar el nuevo servicio en la base de datos
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
    session.clear() # Borra la sesión del usuario
    return redirect(url_for('index')) # Redirige al usuario a la página de inicio de sesión




if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port="5080")
