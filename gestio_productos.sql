CREATE DATABASE gestion_producto;
USE gestion_producto;
SHOW TABLES;

/* DDL CON ENFOQUE EN SEGURIDAD*/
/* creamos un usuario con persimos solo para acceder a la base de datos gestion_producto*/

/* usuario: userGestion1,  password: userGestion-1 */
CREATE USER 'userGestion1'@'localhost' identified by 'userGestion-1';

GRANT ALL PRIVILEGES ON gestion_producto.* TO userGestion1@localhost;
FLUSH PRIVILEGES;

DROP USER 'userGestion1'@'localhost';

/* DDL CON ENFOQUE EN SEGURIDAD*/
/*
CREATE TABLE PRODUCTO(
	codigo CHAR(10) PRIMARY KEY,
    nombre VARCHAR(60) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL,
    proveedor VARCHAR(100) NOT NULL
);

CREATE TABLE productoElectronico(
	codigo CHAR(10) PRIMARY KEY,
    meses_garantia INT NOT NULL,
    FOREIGN KEY (codigo) REFERENCES PRODUCTO(codigo)
);


CREATE TABLE productoAlimenticio(
	codigo CHAR(10) PRIMARY KEY,
    fecha_vencimiento CHAR(7) NOT NULL, 
    FOREIGN KEY (codigo) REFERENCES PRODUCTO(codigo)
);
*/
/*
CREATE TABLE PRODUCTO (
    id INT UNSIGNED AUTO_INCREMENT,
    codigo CHAR(10) NOT NULL,
    nombre VARCHAR(60) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL,
    proveedor VARCHAR(100) NOT NULL,
    PRIMARY KEY(id)
);
CREATE TABLE productoElectronico (
    id INT UNSIGNED AUTO_INCREMENT,
    producto_id INT UNSIGNED NOT NULL, -- Referencia a la tabla PRODUCTO
    meses_garantia INT NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY (producto_id) REFERENCES PRODUCTO(id) ON DELETE CASCADE
);
CREATE TABLE productoAlimenticio (
    id INT UNSIGNED AUTO_INCREMENT,
    producto_id INT UNSIGNED NOT NULL, -- Referencia a la tabla PRODUCTO
    fecha_vencimiento DATE NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY (producto_id) REFERENCES PRODUCTO(id) ON DELETE CASCADE
);

*/

/*
INSERT INTO PRODUCTO (codigo, nombre, precio, stock, proveedor)
                        VALUES (1111, "hola", 10.0, 1000, "hola");

INSERT INTO productoElectronico (producto_id, meses_garantia)
VALUES (1, 6);
*/
/*
-- Insertar datos en la tabla PRODUCTO
INSERT INTO PRODUCTO (codigo, nombre, precio, stock, proveedor) VALUES
('26265265', 'TV', 250005.00, 6, 'LG'),
('24567543', 'HORNO', 250005.00, 6, 'ARG'),
('26265265', 'arroz', 250005.00, 6, 'Marolio'),
('24567543', 'fideo', 250005.00, 6, 'marolio');

INSERT INTO productoElectronico (producto_id, meses_garantia) VALUES
((SELECT id FROM PRODUCTO WHERE codigo = '26265265' AND nombre = 'TV'), 6),
((SELECT id FROM PRODUCTO WHERE codigo = '24567543' AND nombre = 'HORNO'), 6);

INSERT INTO productoAlimenticio (producto_id, fecha_vencimiento) VALUES
((SELECT id FROM PRODUCTO WHERE codigo = '26265265' AND nombre = 'arroz'), '2024-10-27'),
((SELECT id FROM PRODUCTO WHERE codigo = '24567543' AND nombre = 'fideo'), '2024-10-27');


SELECT p.codigo FROM PRODUCTO p
JOIN productoAlimenticio pa ON p.id = pa.producto_id
WHERE p.codigo = '24567543';
*/
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

DROP TABLE PRODUCTO;


update productoElectronico set stock = stock + 2 where codigo = 00; 