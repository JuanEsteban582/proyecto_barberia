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


#----------------------------------BARBERIA REGISTRO--------------------_----#



@app.route('/barberia_registro')
def barberia_registro():
    return render_template('barberia/barberiaR.html')





if __name__ == '__main__':
    app.run(debug=True)

        



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port="5080")