# Desafío 1: Sistema de Gestión de Productos
# Objetivo: Desarrollar un sistema para manejar productos en un inventario.
# Requisitos:
#     • Crear una clase base Producto con atributos como nombre, precio, cantidad en stock, etc.
#     • Definir al menos 2 clases derivadas para diferentes categorías de productos (por ejemplo, ProductoElectronico, ProductoAlimenticio) con atributos y métodos específicos.
#     • Implementar operaciones CRUD para gestionar productos del inventario.
#     • Manejar errores con bloques try-except para validar entradas y gestionar excepciones.
#     • Persistir los datos en archivo JSON.
import json
import os
import inspect
import mysql.connector
from mysql.connector import Error
from decouple import config


class Producto:
    def __init__(self, codigo, nombre, precio,  stock, proveedor):
        '''INICIALIZAMOS EN CONSTRUCTOR'''
        self.__codigo = codigo
        self.__nombre = nombre
        self.__precio = precio
        self.__stock = stock
        self.__proveedor = proveedor

    ### DEFINIMOS GETTER AND SETTER
    @property
    def codigo(self):
        return self.__codigo

    @codigo.setter
    def codigo(self, value):
        self.__codigo = value

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, value):
        self.__nombre = value

    @property
    def precio(self):
        return self.__precio

    @precio.setter
    def precio(self, value):
        self.__precio = value

    @property
    def stock(self):
        return self.__stock

    @stock.setter
    def stock(self, value):
        self.__stock = value

    @property
    def proveedor(self):
        return self.__proveedor

    @proveedor.setter
    def proveedor(self, value):
        self.__proveedor = value

    def to_dict(self):
        '''RETORNAMOS UN DICCIONARIO (CLAVE : VALOR)'''
        return {
            "codigo" : self.codigo,
            "nombre" : self.nombre,
            "precio" : self.precio,
            "stock" : self.stock,
            "proveedor" : self.proveedor
        }


    def obtener_atributos(clase):
        return [param for param in inspect.signature(clase.__init__).parameters if param != 'self']

    def __str__(self):
        '''RETORNAMOS CODIGO Y NOMBRE'''
        return f"Codigo: {self.codigo} - Nombre: {self.nombre} - Stock: {self.stock}"


class ProductoAlimenticio(Producto):
    def __init__(self, codigo, nombre, precio,  stock, proveedor, fecha_vencimiento):
        super().__init__(codigo, nombre, precio,  stock, proveedor)
        self.__fecha_vencimiento = fecha_vencimiento

    @property
    def fecha_vencimiento(self):
        return self.__fecha_vencimiento

    @fecha_vencimiento.setter
    def fecha_vencimiento(self, value):
        self.__fecha_vencimiento = value

    def to_dict(self):
        '''RETORNAMOS UN DICCIONARIO (CLAVE : VALOR) CON UN ELEMENTO MAS'''
        data = super().to_dict()
        data["fecha_vencimiento"] = self.fecha_vencimiento
        return data

    def __str__(self):
        '''RETORNAMOS CODIGO, NOMBRE Y FECHA DE VENCIMIENTO'''
        return f"{super().__str__()} - Fecha de vencimiento: {self.fecha_vencimiento}"


class ProductoElectronico(Producto):
    def __init__(self, codigo, nombre, precio,  stock, proveedor, meses_garantia):
        super().__init__(codigo, nombre, precio,  stock, proveedor)
        self.__meses_garantia = meses_garantia

    @property
    def meses_garantia(self):
        return self.__meses_garantia

    @meses_garantia.setter
    def meses_garantia(self, value):
        self.__meses_garantia = value

    def to_dict(self):
        '''RETORNAMOS UN DICCIONARIO (CLAVE : VALOR) CON UN ELEMENTO MAS'''
        data = super().to_dict()
        data["meses_garantia"] = self.meses_garantia
        return data

    def __str__(self):
        '''RETORNAMOS CODIGO, NOMBRE Y MESES DE GARANTIA'''
        return f"{super().__str__()} - Garantia Validad: {self.meses_garantia} meses"


class CRUDProductos:
    clases_productos = {
        'productoElectronico': ProductoElectronico,
        'productoAlimenticio': ProductoAlimenticio
    }
    # # Especifica la ubicación y el nombre del archivo donde se guardará el JSON
    # directorio = os.getcwd()  # Obtiene el directorio actual
    # nombre_archivo = 'productos.json'
    # ruta_completa = os.path.join(directorio, nombre_archivo)

    def __init__(self):
        self.host = config('DB_HOST')
        self.database = config('DB_NAME')
        self.user = config('DB_USER')
        self.password = config('DB_PASSWORD')
        self.port = config('DB_PORT')

    def connect(self):
        ''' estable conexion con la base de datos '''
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            if connection.is_connected():
                return connection

        except Error as e:
            print(f'Error al conectar con base de datos: {e}')
            return None

    def leer_datos(self):
        try:
            with open(self.archivo, 'r') as file:
                datos = json.load(file)

        except FileNotFoundError: # Maneja el caso cuando el archivo no se encuentra.
            print(f'El archivo {self.archivo} no se encontró.')

        except TypeError as type_error: # Maneja errores de tipo que pueden ocurrir al intentar serializar los datos en JSON.
            print(f'Error de tipo al intentar guardar los datos: {type_error}')

        except json.JSONDecodeError as json_error: # Esto captura específicamente errores al decodificar JSON.
            raise ValueError(f'Error al decodificar el JSON: {json_error}')

        except IOError as io_error: # Esto captura errores de entrada/salida que pueden ocurrir durante la lectura del archivo.
            raise IOError(f'Error de E/S al leer el archivo: {io_error}')

        except Exception as error:
            raise Exception(f'Error inesperado al leer datos del archivo: {error}')

        else:
            return datos

        # except FileNotFoundError:
        #     return {}
        # except Exception as error:
        #     raise Exception(f'Error al leer datos del archivo: {error}')
        # else:
        #     return datos

    def guardar_datos(self, datos):
        try:
            with open(self.archivo, 'w') as file:
                json.dump(datos, file, indent=4)

        except FileNotFoundError: # Maneja el caso cuando el archivo no se encuentra.
            print(f'El archivo {self.archivo} no se encontró.')

        except PermissionError: # Maneja los casos donde no se tienen los permisos necesarios para escribir en el archivo.
            print(f'Permiso denegado para escribir en el archivo {self.archivo}.')

        except TypeError as type_error: # Maneja errores de tipo que pueden ocurrir al intentar serializar los datos en JSON.
            print(f'Error de tipo al intentar guardar los datos: {type_error}')

        except IOError as io_error: # Esto captura errores de entrada/salida que pueden ocurrir durante la lectura del archivo.
            print(f'Error de E/S al intentar guardar los datos en {self.archivo}: {io_error}')

        except Exception as error:
            print(f'Error inesperado: {error}')

        else:
            print(f'Datos guardados exitosamente en {self.archivo}')

        # except IOError as error:
        #     print(f'Error al intentar guardar los datos en {self.archivo}: {error}')
        # except Exception as error: #TODO  HAY QUE SER MAS CLAROS CON LOS TIPOS DE ERRORES
        #     print(f'Error inesperado: {error}')

    def crear_producto(self, producto, categoria): ## SE ENVIARA EL TIPO DE PRODUCTO YA SELECCIONADO EN EL MENU MAIN
        try:
            # Validar que la categoría es una ELEMENTO permitido
            categoria_valida = ['productoElectronico', 'productoAlimenticio']
            if categoria not in categoria_valida:
                print(f"Categoría {categoria} no válida.")
                return

            connection = self.connect()
            if connection:

                with connection.cursor() as cursor:

                    query = f'''
                        SELECT codigo FROM {categoria} WHERE codigo = %s
                    '''
                    cursor.execute(query, (producto.codigo,))

                    if cursor.fetchone():
                        print("YA EXISTE UN PRODUCTO CON ESTE CODIGO.")
                        return

                    if categoria is 'productoElectronico':
                        query = '''
                        INSERT INTO productoElectronico (codigo, nombre, precio, stock, proveedor, meses_garantia)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        '''
                        cursor.execute(query, (producto.codigo, producto.nombre, producto.precio, producto.stock, producto.proveedor, producto.meses_garantia))

                    elif categoria is 'productoAlimenticio':
                        query = '''
                        INSERT INTO productoAlimenticio (codigo, nombre, precio, stock, proveedor, fecha_vencimiento)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        '''
                        cursor.execute(query, (producto.codigo, producto.nombre, producto.precio, producto.stock, producto.proveedor, producto.fecha_vencimiento))

                    connection.commit()
                    print(f'Producto {categoria}, Nombre: {producto.nombre}, Codigo: {producto.codigo} CREADO')

        except Exception as error:
            print(f'Error inesperado: {error}')

        finally:
            if connection:
                connection.close()

    def leer_producto(self, codigo, categoria):

        try:
            connection = self.connect()
            if connection:
                with connection.cursor(dictionary=True) as cursor:
                    query = f'''
                        SELECT * FROM {categoria} WHERE codigo = %s
                    '''
                    cursor.execute(query, (codigo,))
                    producto_tada = cursor.fetchone()


                    if producto_tada:
                        # Obtener la clase correspondiente al nombre de la categoría
                        # clases_productos = { ## original
                        #     'productoElectronico': ProductoElectronico,
                        #     'productoAlimenticio': ProductoAlimenticio
                        # }

                        producto_clase = self.clases_productos.get(categoria)
                        if producto_clase:
                            producto_info = producto_clase(**producto_tada)
                            #print(f'Se encontró PRODUCTO: {producto_info}')
                        else:
                            producto_info = None
                            ## AQUI CUANDO NO SE RECONOCE LA CATEGORIA
                            print(f'Categoría {categoria} no reconocida.')
                    else:
                        ## AQUI CUANDO NO SE ENCUENTRA EL PRODUCTO
                        producto_info = None
                        ## print(f'No se encontró PRODUCTO con CODIGO: {codigo}')

        except Exception as error:
            print(f'Error inesperado: {error}')
        else:
            return producto_info
        finally:
            if connection:
                connection.close()

    def actualizar_producto(self, codigo, categoria):
        try:
            connection = self.connect()

            if connection:

                # PRIMERO buscamos si existe el producto
                if self.leer_producto(codigo, categoria):

                    with connection.cursor(dictionary=True) as cursor:
                        print(self.leer_producto(codigo, categoria))
                        nuevo_ingreso = int(input('Ingrese cantidad del ingreso: '))
                        query = f'''
                            UPDATE {categoria} SET  stock = stock + %s  WHERE codigo = %s
                        '''
                        #update productoElectronico set stock = stock + 2 where codigo = 00;
                        cursor.execute(query, (nuevo_ingreso, codigo,))

                        ## consulta para verificar si se ejecuto el cambio
                        if cursor.rowcount > 0:
                            connection.commit()
                            print("carga de stock actulizada.")
                            print(self.leer_producto(codigo, categoria))
                        else:
                            print("Stock no se logro actualizar.")
                else:
                    print("NO SE ENCONTRO PRODUCTO.")

        except Exception as error:
            print(f'Error inesperado: {error}')
        finally:
            if connection:
                connection.close()

    def eliminar_producto(self, codigo, categoria):
        try:
            connection = self.connect()

            if connection:
                # PRIMERO buscamos si existe el producto
                if self.leer_producto(codigo, categoria):

                    with connection.cursor(dictionary=True) as cursor:
                        print(self.leer_producto(codigo, categoria)) # mostramos el producto a eliminar

                        confirmacion_delete = input('Seguro que desea eliminar? Y/N: ')
                        if confirmacion_delete.lower() == "y":
                            query = f'''
                                DELETE FROM {categoria} WHERE codigo = %s
                            '''
                            cursor.execute(query, (codigo,))

                            ## consulta para verificar si se ejecuto el cambio
                            ## CONSULTA SI EXISTE ALGUN REGISTRO, SI ES ASI, ES PORQUE SE REALIZO LA OPERACION
                            if cursor.rowcount > 0:
                                connection.commit()
                                print("PRODUCTO ELIMINADO.")
                            else:
                                print("No se pudo ELIMINAR el prodcuto.")
                        else:
                            print("SE CANCELA LA ELIMINACION DEL PRODUCTO.")
                else:
                    print("NO SE ENCONTRO PRODUCTO.")

        except Exception as error:
            print(f'Error inesperado: {error}')
        finally:
            if connection:
                connection.close()

    def motrar_todos_productos(self):
        base_datos = {}
        try:
            connection = self.connect()

            if connection:
                with connection.cursor(dictionary=True) as cursor:

                    for categoria, valor in self.clases_productos.items():
                        cursor.execute(f"SELECT * FROM {categoria};")
                        base_datos[categoria] = cursor.fetchall()
                    
                    ## return base_datos
                    ## ORIGINAL
                    # cursor.execute("SELECT * FROM productoElectronico;")
                    # resultados_electronico = cursor.fetchall()

                    # cursor.execute("SELECT * FROM productoAlimenticio;")
                    # resultados_alimenticio = cursor.fetchall()

                    # return {"Productos Electronicos":resultados_electronico, "Productos Alimenticios":resultados_alimenticio}

        except Exception as error:
            print(f'Error inesperado: {error}')
        else:
            return base_datos
        finally:
            if connection:
                connection.close()
