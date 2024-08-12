#from os import name, system
import os
import platform
from time import sleep
from Sistema_Gestio_Producto import ProductoAlimento, ProductoElectronico, CRUDProductos

###################### LIMPIA PANTALLA ######################
# Para Unix/Linux/MacOS/BSD
# if name == "posix":
#     limpiar = "clear"
# # Para DOS/Windows
# elif name == "ce" or name == "nt" or name == "dos":
#     limpiar = "cls"


def limpiar_pantalla():
    ''' Limpiar la pantalla según el sistema operativo'''
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear') # Para Linux/Unix/MacOs

################## ESPERA Y LIMPIEZA #######################

# def sleep_and_clear():
#     """ GENERAMOS UN TIEMPO DE ESPERA Y PUEGO EJECUTAMOS UNA LIMPIEZA DE PANTALLA"""
#     sleep(2)
#     system(limpiar)

# time.sleep(3) tiempo de esperta antes de la siguiente ejecucion
# os.system(limpiar) limpia la pantalla



def menu_ppal():
    limpiar_pantalla()
    menu = input('''
        *******************************************
        *       Sistema Analisis de Datos         *
        *******************************************
        *                                         *
        *     1 - Add Producto                    *
        *     2 - Buscar Producto X codigo        *
        *     3 - Alctualizar Stock               *
        *     4 - Eliminar Producto               *
        *     5 - Mostrar Productos               *
        *     6 - Salir                           *
        *                                         *
        *******************************************
    Ingrese una opción: ''')
    # limpiar_pantalla()
    return menu


def menu_categoria():
    limpiar_pantalla()
    #opciones = ['1','2','3'] #ORIGINAL
    opciones = {
        '1': 'productoElectronico',
        '2': 'productoAlimenticio'
        }
    while True:
        menu = input('''
            *******************************************
            *          MENU TIPO DE PRODUCTO          *
            *******************************************
            *                                         *
            *     1 - Producto Electro                *
            *     2 - Producto Alimento               *
            *     3 - Salir                           *
            *                                         *
            *******************************************
        Ingrese una opción: ''')
        if str(menu) in opciones:
            #return menu.values()
            limpiar_pantalla()
            return opciones[menu]
        elif menu == '3': #TODO HAY QUE MEJORAR EL SALIR
            limpiar_pantalla()
            menu_ppal()
        else:
            print('Opción no válida. Por favor, seleccione una opción válida')
            

def agregar_producto(control_productos, categoria):
    try:
        
        codigo = input('Ingrese CODIG: ')
        nombre = input('Ingrese NOMBRE: ')
        precio = float(input('Ingrese PRECIO: '))
        stock = int(input('Ingrese Cantidad de STOCK: ') )
        proveedor = input('Ingrese PROVEEDOR: ')
        
        if categoria == 'productoElectronico':
            meses_garantia = input('Ingrese Meses de Garantia: ')
            producto = ProductoElectronico(codigo, nombre, precio,  stock, proveedor, meses_garantia)
        elif categoria == 'productoAlimenticio':
            fecha_vencimiento = input('Ingrese Fecha de Vencimiento DD/MM/AAAA: ')
            producto = ProductoAlimento(codigo, nombre, precio,  stock, proveedor, fecha_vencimiento)
        else:
            print("OCURRIO UN ERROR !ENTRO POR ACA!.")

        control_productos.crear_producto(producto, categoria)
        input('ENTER para continuar...')
       

    except Exception as error: #TODO HAY QUE SER MAS CLAROS CON LOS TIPOS DE ERRORES
            print(f'Error inesperado: {error}')

def buscar_producto_por_codigo(control_productos, categoria):
    codigo = input('Ingrese el CODIGO del PRODUCTO: ')
    control_productos.leer_producto(codigo, categoria)
    input('Presione enter para continuar...')

def actualizar_stock(control_productos, categoria):
    codigo = input('Ingrese el CODIGO del PRODUCTO: ')
    control_productos.actualizar_producto(codigo, categoria)
    input('Presione enter para continuar...')

def eliminar_producto_por_codigo(control_productos,categoria):
    codigo = input('Ingrese el CODIGO del PRODUCTO: ')
    control_productos.eliminar_producto(codigo, categoria)
    input('Presione enter para continuar...')

def mostrar_todos_los_productos(control_productos):
    print('=============== Listado completo de los PRODUCTOS =============== ')
    #producto = control_productos.leer_datos()#ORIGINAL
    #for categoria, productos in producto.items(): #ORIGINAL
    for categoria, productos in control_productos.leer_datos().items():
        print(f"Categoría: {categoria}")
        for producto_id, detalles in productos.items():
            print(f"  Producto ID: {producto_id}")
            for key, value in detalles.items():
                print(f"    {key}: {value}")
    print('================================================================== ')
    input('Presione enter para continuar...')


if __name__ == "__main__":
    # json_productos = 'productos_db.json'
    # control_productos = CRUDProductos(json_productos)
    control_productos = CRUDProductos()

    while True:
        opcion = menu_ppal()
        if opcion == '1': # AGREGAR PRODUCTO
            categoria = menu_categoria()
            agregar_producto(control_productos, categoria)

        elif opcion == "2": # BUSCAR POR CODIGO
            categoria = menu_categoria()
            buscar_producto_por_codigo(control_productos, categoria)
            
        elif opcion == "3": # ACTUALIZAR
            categoria = menu_categoria()
            actualizar_stock(control_productos, categoria)

        elif opcion == "4": # ELIMINAR PRODUCTO
            categoria = menu_categoria()
            eliminar_producto_por_codigo(control_productos,categoria)

        elif opcion == "5": # MOSTRAR TODOS LOS PRODUCTOS
            mostrar_todos_los_productos(control_productos)

        elif opcion == "6": # SALIR
            print('Saliendo del programa...')
            break
        
        else: # NO VALIDO
            system(limpiar)
            print('Opción no válida. Por favor, seleccione una opción válida (1-7)')
            
        


