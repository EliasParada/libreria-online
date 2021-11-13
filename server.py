import mysql.connector
import json
import math

from urllib import parse
from http.server import HTTPServer, SimpleHTTPRequestHandler

class crud():
    def __init__(self):
        self.sesion = {'inicio': False, 'usuario':'None', 'contra':'None'}
        self.conn = mysql.connector.connect(host = 'localhost', user = 'root', port = 3307, password = '', database = 'book_store')
        if self.conn.is_connected():
            print('Conectado a la base de datos')
        else:
            print('No se pudo conectar a la base de datos')

    def ejecutar_sql(self, sql, valores):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, valores)
            self.conn.commit()
            print('Se ejecuto la consulta')
            return True
        except Exception as e:
            print(e)
            return False

    def ejecutar_mostrar_sql(self, sql):
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(sql)
            resultado = cursor.fetchall()
            print(cursor.fetchall())
            print(resultado)
            if len(resultado) == 0:
                return False, resultado
            else:
                return True, resultado
        except Exception as e:
            print(e)
            return False

    def ejecutar_select_datos(self, sql, datos):
        try:
            print(sql)
            print(datos)
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(sql, datos)
            resultado = cursor.fetchall()
            print(resultado)
            if len(resultado) == 0:
                return False, resultado
            else:
                return True, resultado
        except Exception as e:
            print(e)
            return False

    def administrar_libros(self, datos):
        if datos['accion'] == 'insertar':
            sql = 'INSERT INTO libros (idLibro, Titulo, Autor, Edicion, Sinopsis, Imagen, Cantidad) VALUES (%s, %s, %s, %s, %s, %s, %s)'
            valores = (datos['id'], datos['titulo'], datos['autor'], datos['edicion'], datos['sinopsis'], datos['imagen'], datos['cantidad'])
            return self.ejecutar_sql(sql, valores)
        
        elif datos['accion'] == 'actualizar':
            sql = 'UPDATE libros SET Titulo = %s, Autor = %s, Edicion = %s, Sinopsis = %s, Imagen = %s, Cantidad = %s WHERE idLibro = %s'
            valores = (datos['titulo'], datos['autor'], datos['edicion'], datos['sinopsis'], datos['imagen'], datos['cantidad'], datos['id'])
            return self.ejecutar_sql(sql, valores)

        elif datos['accion'] == 'eliminar':
            sql = 'DELETE FROM libros WHERE idLibro = %s'
            valores = (datos['id'],)
            return self.ejecutar_sql(sql, valores)

        elif datos['accion'] == 'mostrar':
            sql = 'SELECT libros.idLibro, libros.Titulo, libros.Autor, libros.Edicion, libros.Sinopsis, libros.Imagen, libros.Cantidad, GROUP_CONCAT(generos.Nombre) AS Generos FROM libros LEFT JOIN generolibro ON libros.idLibro = generolibro.idLibro LEFT JOIN generos ON generolibro.idGenero = generos.idGenero GROUP BY libros.idLibro'
            return self.ejecutar_mostrar_sql(sql)

    def administrar_cuentas(self, datos):
        if datos['accion'] == 'insertar':
            sql = 'INSERT INTO usuarios (idUsuario, Dui, Nombre, Nickname, Telefono, Correo, Direccion, FechaNacimiento, Contraseña, idTipo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            valores = (datos['id'], datos['dui'], datos['nombre'], datos['nickname'], datos['telefono'], datos['correo'], datos['direccion'], datos['fechaNacimiento'], datos['contraseña'], datos['idTipo'])
            return self.ejecutar_sql(sql, valores)
        
        elif datos['accion'] == 'actualizar':
            sql = 'UPDATE usuarios SET Dui = %s, Nombre = %s, Nickname = %s, Telefono = %s, Correo = %s, Direccion = %s, FechaNacimiento = %s, Contraseña = %s, idTipo = %s WHERE idUsuario = %s'
            valores = (datos['dui'], datos['nombre'], datos['nickname'], datos['telefono'], datos['correo'], datos['direccion'], datos['fechaNacimiento'], datos['contraseña'], datos['idTipo'], datos['id'])
            return self.ejecutar_sql(sql, valores)

        elif datos['accion'] == 'eliminar':
            sql = 'DELETE FROM usuarios WHERE idUsuario = %s'
            valores = (datos['id'],)
            return self.ejecutar_sql(sql, valores)

        elif datos['accion'] == 'mostrar':
            sql = 'SELECT * FROM usuarios'
            return self.ejecutar_mostrar_sql(sql)

    def administrar_prestamos(self, datos):
        if datos['accion'] == 'insertar':
            sql = 'UPDATE libros SET Cantidad = Cantidad - 1 WHERE idLibro = %s'
            valores = (datos['idLibro'],)
            self.ejecutar_sql(sql, valores)
            sql = 'INSERT INTO prestamos (idPrestamo, idUsuario, idLibro, FechaPrestamo, FechaDevolusion) VALUES (%s, %s, %s, %s, %s)'
            valores = (datos['id'], datos['idUsuario'], datos['idLibro'], datos['fechaPrestamo'], datos['fechaDevolusion'])
            return self.ejecutar_sql(sql, valores)
        
        elif datos['accion'] == 'actualizar':
            sql = 'UPDATE prestamos SET idUsuario = %s, idLibro = %s, FechaPrestamo = %s, FechaDevolusion = %s WHERE idPrestamo = %s'
            valores = (datos['idUsuario'], datos['idLibro'], datos['fechaPrestamo'], datos['fechaDevolusion'], datos['id'])
            return self.ejecutar_sql(sql, valores)

        elif datos['accion'] == 'eliminar':
            sql = 'DELETE FROM prestamos WHERE idPrestamo = %s'
            valores = (datos['idPrestamo'],)
            return self.ejecutar_sql(sql, valores)

        elif datos['accion'] == 'mostrar':
            sql = 'SELECT prestamos.idPrestamo, libros.idLibro, libros.Titulo, usuarios.idUsuario, usuarios.Nombre, tipoCuenta.Descripcion AS Tipo_Cuenta, prestamos.FechaPrestamo, prestamos.FechaDevolusion FROM prestamos INNER JOIN libros ON prestamos.idLibro = libros.idLibro INNER JOIN usuarios ON prestamos.idUsuario = usuarios.idUsuario INNER JOIN tipoUsuario ON usuarios.idTipo = tipoCuenta.idTipo'
            return self.ejecutar_mostrar_sql(sql)

    def administrar_tipo_cuentas(self, datos):
        if datos['accion'] == 'insertar':
            sql = 'INSERT INTO tipocuenta (idTipo, Descripcion) VALUES (%s, %s)'
            valores = (datos['id'], datos['descripcion'])
            return self.ejecutar_sql(sql, valores)
        
        elif datos['accion'] == 'actualizar':
            sql = 'UPDATE tipocuenta SET Descripcion = %s WHERE idTipo = %s'
            valores = (datos['descripcion'], datos['id'])
            return self.ejecutar_sql(sql, valores)

        elif datos['accion'] == 'eliminar':
            sql = 'DELETE FROM tipocuenta WHERE idTipo = %s'
            valores = (datos['id'],)
            return self.ejecutar_sql(sql, valores)

        elif datos['accion'] == 'mostrar':
            sql = 'SELECT * FROM tipocuenta'
            return self.ejecutar_mostrar_sql(sql)

    def administra_generos(self, datos):
        if datos['accion'] == 'insertar':
            sql = 'INSERT INTO generos (idGenero, Nombre, Descripcion) VALUES (%s, %s, %s)'
            valores = (datos['id'], datos['nombre'], datos['descripcion'])
            return self.ejecutar_sql(sql, valores)
        
        elif datos['accion'] == 'actualizar':
            sql = 'UPDATE generos SET Nombre = %s, Descripcion = %s WHERE idGenero = %s'
            valores = (datos['nombre'], datos['descripcion'], datos['id'])
            return self.ejecutar_sql(sql, valores)

        elif datos['accion'] == 'eliminar':
            sql = 'DELETE FROM generos WHERE idGenero = %s'
            valores = (datos['id'],)
            return self.ejecutar_sql(sql, valores)

        elif datos['accion'] == 'mostrar':
            sql = 'SELECT * FROM generos'
            return self.ejecutar_mostrar_sql(sql)

    def administrar_estanterias(self, datos):
        if datos['accion'] == 'insertar':
            sql = 'INSERT INTO estanteria (idUsuario, idLibro) VALUES (%s, %s)'
            valores = (datos['idUsuario'], datos['idLibro'])
            return self.ejecutar_sql(sql, valores)
        
        elif datos['accion'] == 'actualizar':
            sql = 'UPDATE estanteria SET idUsuario = %s, idLibro = %s WHERE idUsuario = %s AND idLibro = %s'
            valores = (datos['idUsuario'], datos['idLibro'], datos['idUsuario'], datos['idLibro'])
            return self.ejecutar_sql(sql, valores)

        elif datos['accion'] == 'eliminar':
            sql = 'DELETE FROM estanteria WHERE idUsuario = %s AND idLibro = %s'
            valores = (datos['idUsuario'], datos['idLibro'])
            return self.ejecutar_sql(sql, valores)

        elif datos['accion'] == 'mostrar':
            sql = 'SELECT estanteria.idUsuario, estanteria.idLibro, libros.idLibro, libros.Titulo, usuarios.idUsuario, usuarios.Nombre FROM estanteria INNER JOIN libros ON estanteria.idLibro = libros.idLibro INNER JOIN usuarios ON estanteria.idUsuario = usuarios.idUsuario'
            return self.ejecutar_mostrar_sql(sql)

    def administrar_prediccion(self, datos):
        sql = 'SELECT libros.Titulo, generos.Nombre, libro.Autor, libros.Sinopsis, libros.Imagen FROM libros INNER JOIN generolibro ON libros.idLibro = generolibro.idLibro INNER JOIN generos ON generolibro.idGenero = generos.idGenero INNER JOIN autores ON libros.idAutor = autores.idAutor WHERE generos.idGenero = %s'
        valores = (datos['idGenero'],)
        return self.ejecutar_select_datos(sql, valores)

    def registro(self):
        if self.sesion['inicio'] == True:
            return True
        else:
            return False
        
    def salir(self):
        if self.sesion['inicio'] == False:
            return True
        else:
            return False

    def administrar_sesion(self, datos):
        print(self.sesion)
        # if datos['iniciar']:
        sql = 'SELECT * FROM usuarios WHERE Nickname = %s AND Contraseña = %s'
        valores = (datos['usuario'], datos['contra'])
        resultado = self.ejecutar_select_datos(sql, valores)
        if resultado[0] == True:
            self.sesion['inicio'] = True
            self.sesion['usuario'] = resultado[1][0]['Nickname']
            self.sesion['contra'] = resultado[1][0]['Contraseña']
            return True
        else:
            return False
        # else:
        #     return True


crud = crud()

class servidorBasico(SimpleHTTPRequestHandler):
    def do_GET(self):
        print(crud.registro())
        print(self.path)
        if self.path == '/':
            if crud.registro() == False:
                print('error')
                self.path = '/login.html'
                return SimpleHTTPRequestHandler.do_GET(self)
            else:
                print('entro')
                self.path = '/index.html'
                return SimpleHTTPRequestHandler.do_GET(self)

        #Si el path es /login entonces mostrar el login.html
        elif self.path == '/login':
            if crud.registro() == True:
                self.path = '/index.html'
                return SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.path = '/login.html'
                return SimpleHTTPRequestHandler.do_GET(self)
        
        #Si el path es /logout entonces cerrar la sesion
        elif self.path == '/logout':
            crud.registro({'inicio': True})
            self.path = '/login.html'
            return SimpleHTTPRequestHandler.do_GET(self)

        #Si el path es estanteria, recomendaciones, tendencias o cuenta y se esta logeado entonces mostrar el el path que se solicita
        elif self.path == '/index' or self.path == '/estanteria' or self.path == '/recomendaciones' or self.path == '/tendencias' or self.path == '/cuenta':
            if crud.registro() == True:
                if self.path == '/index':
                    self.path = '/index.html'
                    return SimpleHTTPRequestHandler.do_GET(self)
                if self.path == '/cuenta':
                    self.path = '/cuenta.html'
                    return SimpleHTTPRequestHandler.do_GET(self)
                elif self.path == '/estanteria':
                    self.path = '/estanteria.html'
                    return SimpleHTTPRequestHandler.do_GET(self)
                elif self.path == '/recomendaciones':
                    self.path = '/recomendaciones.html'
                    return SimpleHTTPRequestHandler.do_GET(self)
                elif self.path == '/tendencias':
                    self.path = '/tendencias.html'
                    return SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.path = '/login.html'
                return SimpleHTTPRequestHandler.do_GET(self)

        elif self.path == '/mostra_libros':
            if crud.registro() == True:
                result = crud.administrar_libros({'accion':'mostrar'})
                print(result)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps(result).encode('utf-8'))
            else:
                self.path = '/login.html'
                return SimpleHTTPRequestHandler.do_GET(self)
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        body = parse.unquote(body.decode('utf-8'))
        print(body)
        body = json.loads(body)
        print(self.path)

        if self.path == '/iniciar_sesion':
            result = crud.administrar_sesion(body)
            if result:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(bytes(json.dumps({'inicio':result}), 'utf-8'))
            else:
                print('Error')
        
        elif self.path == '/logout':
            if crud.registro() == True:
                crud.salir()
                self.path = '/login.html'
                return SimpleHTTPRequestHandler.do_GET(self)
            
        elif self.path == '/administrar_usuarios':
            result = crud.administrar_cuentas(body)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(json.dumps(result), 'utf-8'))

        elif self.path == '/administrar_generos':
            result = crud.administra_generos(body)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(json.dumps(result), 'utf-8'))
        
        elif self.path == '/administrar_tipocuenta':
            result = crud.administrar_tipo_cuentas(body)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(json.dumps(result), 'utf-8'))
        
        elif self.path == '/administrar_libros':
            result = crud.administrar_libros(body)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(json.dumps(result), 'utf-8'))

        elif self.path == '/administrar_prestamos':
            result = crud.administrar_prestamos(body)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(json.dumps(result), 'utf-8'))
        
        elif self.path == '/administrar_estanterias':
            result = crud.administrar_estanterias(body)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(json.dumps(result), 'utf-8'))

        elif self.path == '/administrar_recomendaciones' or self.path == '/administrar_tendencias':
            result = crud.administrar_prediccion(body)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(json.dumps(result), 'utf-8'))

print('Iniciando servidor')
httpd = HTTPServer(('localhost', 3000), servidorBasico)
httpd.serve_forever()