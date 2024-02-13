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
    rol = request.form['tipo_registro']

    if rol == 'cliente':
        sql = f"SELECT contrasena,correo FROM usuario WHERE correo='{email}'"
    elif rol == 'propietario':
        sql = f"SELECT contrasena_P,correo_P FROM propietario WHERE correo_P='{email}'"
    elif rol == 'barbero':
        sql = f"SELECT bcontrasena,bcorreo FROM barberos WHERE bcorreo='{email}'"
    else:
        return render_template('login.html')  # Manejar caso no reconocido

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchone()
    conn.commit()

    if resultado and contrasena == resultado[0]:
        session["logueado"] = True
        session["usuario_id"] = email
        session["usuario_nombre"] = resultado[1]  # Tomar el nombre del resultado
        if rol == 'cliente':
            return render_template('htmls_principal_page/principal_cliente.html')
        elif rol == 'propietario':
            return render_template('htmls_principal_page/principal_propietario.html')
        elif rol == 'barbero':
            return render_template('htmls_principal_page/principal_barbero.html')

    return render_template('login.html')
    
    
    

        #----//REGISTRO DE DATOS Y MANEJO DE ROLES EN EL REGISTRO-------//;
        #//------SE LLEVARA UNA SOLA INTERFAZ DE REGISTRO PARA EL USUARIO-------- //#
        
@app.route("/registro", methods=['GET','POST'])
def registro():
    if request.method == 'POST':
        fk_cedula = request.form['cedula_registro']
      
       #SENTENCIA DE SQL PARA VERIFICAR SI EXISTEN LOS DOCUMENTOS EN LA TABLA BARBERO, CLIENTE, PROPIETARIO //
       
       #SE IBA A HACER CON INNER JOIN PERO A LO ULTIMO LAS HICE POR SERPARADO LAS CONSULTAS 
        sqlU_ced_existe = f"SELECT fk_cedulaU FROM usuario WHERE fk_cedulaU = %s"  
        sqlB_ced_existe = f"SELECT fk_cedulaB FROM barberos WHERE fk_cedulaB = %s" 
        sqlP_ced_existe = f"SELECT pk_cedulaP FROM propietario WHERE pk_cedulaP = %s" 
        
        nombre = request.form['nombre_usuario']
        apellidos = request.form['apellidos_usuario']
        celular = request.form['celular_usuario']
        ciudad = request.form['ciudad_U']
        rol= request.form['tipo_registro']
        f_nacimiento = request.form['f_nacimiento_U']
        correo = request.form['correo_usuario']
        contrasena = request.form['contrasena']
        confir_contra = request.form['confir_contra']
        tipo_registro = request.form['tipo_registro']
        
        conn = mysql.connect()
        cursor = conn.cursor()
        
        cursor.execute(sqlU_ced_existe, (fk_cedula,))
        usuario_existe = cursor.fetchone()
        
        cursor.execute(sqlB_ced_existe, (fk_cedula,))
        barbero_existe = cursor.fetchone()
        
        
        cursor.execute(sqlP_ced_existe, (fk_cedula,))
        propietario_existe = cursor.fetchone()
        conn.commit()
        
       
        
        
        #calcular edad
        fecha_nacimiento = datetime.strptime(f_nacimiento, '%Y-%m-%d')
        fecha_actual = datetime.now()
        edad_calc = fecha_actual.year - fecha_nacimiento.year - ((fecha_actual.month, fecha_actual.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        
        #VERIFICACIONES 
        
        
        #---//Verifica si la cedula ya existe en alguna de las tres  tablas , ya que la cedula es unica y no se puede repetir
        #En ninguna de las tres tablas -----// 
        if usuario_existe or barbero_existe or propietario_existe :
            msj_error = "La cédula ya está registrada. Introduce una cédula válida."
            return render_template('/registro.html', msj=msj_error)
        
        
        
        if tipo_registro == 'cliente':
            # -------  Realiza el registro en la tabla de CLIENTES ------//
            t_sql = "INSERT INTO usuario (nombre, apellidos, celular, ciudad, f_nacimiento, correo, contrasena, rol, fk_cedulaU) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)"
        
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(t_sql, (nombre, apellidos, celular, ciudad, f_nacimiento, correo, contrasena, rol, fk_cedula))
            conn.commit()
            
        elif tipo_registro == 'barbero':
            # ------ Realiza el registro en la tabla de BARBEROS -------///
            t_bsql = "INSERT INTO barberos (bnombre, apellido, bcelular, bciudad, bf_nacimiento, bcorreo, bcontrasena, rol, fk_cedulaB) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)"
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(t_bsql, (nombre, apellidos, celular, ciudad, f_nacimiento, correo, contrasena, rol, fk_cedula))
            conn.commit()
            
        elif tipo_registro == 'propietario':
            #//--------- Realiza el registro en la tabla de PROPIETARIO------//
            t_Psql = "INSERT INTO propietario (nombre_P,  apellido_P, celular_P, Pciudad,Pf_nacimiento, correo_P, contrasena_P, rol, pk_cedulaP) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)"
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(t_Psql, (nombre, apellidos, celular, ciudad, f_nacimiento, correo, contrasena, rol, fk_cedula))
            conn.commit()
            
            
        else:
            error = "Por favor escoge tu rol"
            return render_template('/registro.html', tmsj=error)
    
        #verifica si la contraseña coincide con la confirmacion de la contra
        if contrasena == confir_contra:
            #----//verificacion si es mayor de edad-----// 
            if edad_calc >=18:
                
                return render_template('login.html')
            else:
                mensaje_edad =" No te puedes registrar por que no eres mayor de 18 años"
                return render_template('registro.html',msjedad = mensaje_edad)
        
        else:
            mensaje_error = "La contraseña y la confirmación de contraseña no coinciden. Inténtalo de nuevo."
            return render_template('registro.html', mensaje=mensaje_error )
            
        
    elif request.method == 'GET':
        return render_template('/registro.html')
        
    
        
        


@app.route("/recuperar_contra", methods=['GET', 'POST'])
def actualizar_contrasena():
    if request.method == 'POST':
        cedula = request.form['cedula_user']
        f_nacimiento = request.form['nacimiento_user']
        f_nacimiento = datetime.strptime(f_nacimiento, '%Y-%m-%d').date()
        nueva_contra = request.form['nueva_contra']
        rol =  request.form['rol_user']
        
        conn = mysql.connect()
        cursor = conn.cursor()

        if rol == 'cliente':
            sql_verificar_cliente = "SELECT fk_cedulaU FROM usuario WHERE fk_cedulaU = %s AND f_nacimiento = %s"
            cursor.execute(sql_verificar_cliente, (cedula, f_nacimiento))
            resultado1 = cursor.fetchone()
            if resultado1:
                sql_actualizacion_cliente = "UPDATE usuario SET contrasena = %s WHERE fk_cedulaU = %s"
                cursor.execute(sql_actualizacion_cliente, (nueva_contra, cedula))
                conn.commit()
                exitoso = "Tu contraseña ha sido actualizada con éxito."
                return render_template('login.html', exito=exitoso)

        elif rol == 'barbero':
            sql_verificar_barbero = "SELECT fk_cedulaB FROM barberos WHERE fk_cedulaB = %s AND bf_nacimiento = %s"
            cursor.execute(sql_verificar_barbero, (cedula, f_nacimiento))
            resultado_barbero = cursor.fetchone()

            if resultado_barbero:
                sql_actualizacion_barbero = "UPDATE barberos SET bcontrasena = %s WHERE fk_cedulaB = %s"
                cursor.execute(sql_actualizacion_barbero, (nueva_contra, cedula))
                conn.commit()
                exitoso = "Tu contraseña ha sido actualizada con éxito."
                return render_template('login.html', exito=exitoso)
            
            
        
        elif rol == 'propietario':
            sql_verificar_propietario = "SELECT pk_cedulaP FROM propietario WHERE pk_cedulaP = %s AND Pf_nacimiento = %s"
            cursor.execute(sql_verificar_propietario, (cedula, f_nacimiento))
            resultado_propietario = cursor.fetchone()

            if resultado_propietario:
                sql_actualizacion_propietario = "UPDATE propietario SET contrasena_P = %s WHERE pk_cedulaP = %s"
                cursor.execute(sql_actualizacion_propietario, (nueva_contra, cedula))
                conn.commit()
                exitoso = "Tu contraseña ha sido actualizada con éxito."
                return render_template('login.html', exito=exitoso)
            

        
        else:
            #mensaje error si la información proporcionada no coincide
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

    # Consulta para recuperar datos del usuario por correo
    sql_usuario = f"SELECT * FROM usuario WHERE correo='{email}'"

    cursor.execute(sql_usuario)
    datos_usuario = cursor.fetchone()

    conn.commit()

    if datos_usuario:
        # Renderizar el perfil del usuario con los datos obtenidos
        return render_template('perfiles/perfil_usuario.html', datos_usuario=datos_usuario)
    else:
        return "Usuario no encontrado", 404


@app.route('/perfil_barbero')
def perfil_barbero():
    if not session.get("logueado"):
        return render_template('login.html')

    email = session.get("usuario_id")
    conn = mysql.connect()
    cursor = conn.cursor()

    # Consulta para recuperar datos del barbero por correo
    sql_barbero = f"SELECT * FROM barberos WHERE bcorreo='{email}'"

    cursor.execute(sql_barbero)
    datos_barbero = cursor.fetchone()

    conn.commit()

    if datos_barbero:
        # Renderizar el perfil del barbero con los datos obtenidos
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

    # Consulta para recuperar datos del propietario por correo
    sql_propietario = f"SELECT * FROM propietario WHERE correo_P='{email}'"

    cursor.execute(sql_propietario)
    datos_propietario = cursor.fetchone()

    conn.commit()

    if datos_propietario:
        # Renderizar el perfil del propietario con los datos obtenidos
        return render_template('perfiles/perfil_propietario.html', datos_propietario=datos_propietario)
    else:
        return "Propietario no encontrado", 404


            #------------------------PAGINAS PRINCIPALES-----------------------------#


@app.route('/principal_cliente')
def principal_cliente():
        return render_template('htmls_principal_page/principal_cliente.html')

@app.route('/principal_propietario')
def principal_propietario():
        return render_template('htmls_principal_page/principal_propietario.html')
    
    
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
        edit_nombre = request.form['nom_U']
        edit_apellidos = request.form['apelli_U']
        edit_celular = request.form['Tel_U']
        edit_ciudad = request.form['ciudad_U']
        edit_fecha_nacimiento = request.form['fech_n_U']

        conn = mysql.connect()
        cursor = conn.cursor()
        
        # Consulta SQL para actualizar los datos del usuario
        sql_act_U = f"UPDATE usuario SET  nombre='{edit_nombre}', apellidos='{edit_apellidos}', celular='{edit_celular}', ciudad='{edit_ciudad}', f_nacimiento='{edit_fecha_nacimiento}' WHERE fk_cedulaU='{edit_cedula}'"
        
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
        edit_nombre = request.form['nom_B']
        edit_apellidos = request.form['apelli_B']
        edit_celular = request.form['Tel_B']
        edit_ciudad = request.form['ciudad_B']
        edit_fecha_nacimiento = request.form['fech_n_B']

        conn = mysql.connect()
        cursor = conn.cursor()
        
        # Consulta SQL para actualizar los datos del usuario
        sql_act_B = f"UPDATE barberos SET  bnombre='{edit_nombre}', apellido='{edit_apellidos}', bcelular='{edit_celular}', bciudad='{edit_ciudad}', bf_nacimiento='{edit_fecha_nacimiento}' WHERE fk_cedulaB='{edit_cedula}'"
        
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
        edit_nombre = request.form['nom_P']
        edit_apellidos = request.form['apelli_P']
        edit_celular = request.form['Tel_P']
        edit_ciudad = request.form['ciudad_P']
        edit_fecha_nacimiento = request.form['fech_n_P']

        conn = mysql.connect()
        cursor = conn.cursor()
        
        # Consulta SQL para actualizar los datos del usuario
        sql_act_P = f"UPDATE propietario SET  nombre_P='{edit_nombre}', apellido_P='{edit_apellidos}', celular_P='{edit_celular}', Pciudad='{edit_ciudad}', Pf_nacimiento='{edit_fecha_nacimiento}' WHERE pk_cedulaP='{edit_cedula}'"
        
        cursor.execute(sql_act_P)
        conn.commit()

        return redirect('/perfil_propietario')
    else:
        email_propietario = session.get("usuario_id")
        conn = mysql.connect()
        cursor = conn.cursor()
        select_p = f"SELECT * FROM propietario WHERE correo_P='{email_propietario}'"
        cursor.execute(select_p)
        datos_propietario = cursor.fetchone()
        conn.commit()

        if datos_propietario:
            return render_template('Actualizacion_perfiles/editar_perfil_propietario.html', datos_propietario=datos_propietario)
        else:
            return "Usuario no encontrado", 404







#----------------------------------BARBERIA REGISTRO--------------------_----#



@app.route('/barberia_registro',methods=['GET', 'POST'])
def barberia_registro():
    if request.method == 'POST':
        nombre_barberia = request.form['nombre_barberia']
        direccion_barberia = request.form['direccion_barberia']
        ciudad_negocio = request.form['ciudad_negocio']
        telefono_negocio = request.form['telefono_negocio']
        pais_negocio = request.form['Pais_negocio']
        departamento_negocio = request.form['departamento_negocio']
        correo_propietario = request.form['correo_negocio']
        hora_apertura = request.form['hora_A']
        hora_cierre = request.form['hora_C']
        
        # Consultar la base de datos para obtener la información del propietario
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT pk_cedulaP, Pf_nacimiento, correo_P FROM propietario WHERE correo_P = '{correo_propietario}'")
        propietario_info = cursor.fetchone()
        
        if propietario_info:
            cedula_propietario = propietario_info[0]
            fecha_nacimiento_propietario = propietario_info[1]
            correo_propietario = propietario_info[2]
        else:
            return "El propietario no está registrado.", 404
        
        # Crear el código único
        codigo_unico = f"{nombre_barberia}-{cedula_propietario}-{fecha_nacimiento_propietario}-{correo_propietario}"
        
        # Verificar si el código único ya existe en la tabla barberias
        cursor.execute(f"SELECT * FROM barberia WHERE pk_codigo_barberia = '{codigo_unico}'")
        existencia = cursor.fetchone()
        
        if existencia:
            mensaje = "La barbería ya está registrada."
            return render_template('registro.html', mensaje=mensaje)
        else:
            # Registrar la barbería con el código único en la tabla barberias
            cursor.execute("INSERT INTO barberia (nom_barberia, direccion, ciudad, telefono, pais, departamento, pk_codigo_barberia, h_apertura, h_cierre) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (nombre_barberia, direccion_barberia, ciudad_negocio, telefono_negocio, pais_negocio, departamento_negocio, codigo_unico, hora_apertura, hora_cierre))
            conn.commit()
            conn.close()

            mensaje = "La barbería se registró exitosamente."
            return render_template('htmls_principal_page/principal_propietario.html', mensaje=mensaje)
    
    return render_template('barberia/barberiaR.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port="5080")