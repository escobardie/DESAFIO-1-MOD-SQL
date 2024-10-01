CREATE DATABASE gestion_producto;
USE gestion_producto;
SHOW TABLES;

/* DDL CON ENFOQUE EN SEGURIDAD*/
/* creamos un usuario con permisos solo para acceder a la base de datos gestion_producto*/

/* usuario: userGestion1,  password: userGestion-1 */
CREATE USER 'userGestion1'@'localhost' identified by 'userGestion-1';

GRANT ALL PRIVILEGES ON gestion_producto.* TO userGestion1@localhost;
FLUSH PRIVILEGES;

DROP USER 'userGestion1'@'localhost';

/* DDL CON ENFOQUE EN SEGURIDAD*/

CREATE TABLE productoElectronico (
    codigo CHAR(10) NOT NULL,
    nombre VARCHAR(60) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL,
    proveedor VARCHAR(100) NOT NULL,
    meses_garantia INT NOT NULL,
    PRIMARY KEY(codigo)
);
CREATE TABLE productoAlimenticio (
    codigo CHAR(10) NOT NULL,
    nombre VARCHAR(60) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL,
    proveedor VARCHAR(100) NOT NULL,
    fecha_vencimiento CHAR(7) NOT NULL, -- MM/AAAA
    PRIMARY KEY(codigo)
);


SELECT * FROM productoElectronico;
SELECT * FROM productoAlimenticio;
