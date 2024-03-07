# SQL y MySQL

- Para ingresar a la terminal de mysql
```bash
mysql -u root -h localhost -p
```

- Este comando se usa para consultar las bases de datos que existen
```bash
show databases

MariaDB [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
4 rows in set (0,001 sec)
```

- Para usar una base da detos se ejecuta este comando:
```bash
use [nombre_base]
```
- Este comando muestra la base de datos que se tiene seleccionanda. En particular se ponen parantesis porque es una funcion. 



### Tipos de tablas
1. MyISAM: directa, sencilla, más rápida y las transacciones son completamente uno a uno
2. InnoDB: nueva, recuperable en caso de falla de disco duro pero es un poco más lenta.

###tipos de tablas
- Talaba de catalogo
    - Tabla que crecerá en un orden lento, según las necesidades de la propia BD. (Listado de Usuarios, InnoDB)
- Tabla de operacion
    - Tabla que se enfoca a lectura, mayor acceso a disco duro. (Prestamos de libros, MyISAM).



### Crear una base de datos


```bash
CREATE database platzi_opration;
```

- Crea la tabla si no existe. 
```bash
CREATE DATABASE IF NOT EXISTS platzi_operation;
```

- Si sale este warning, se puede revisar con este conando:
```bash
SHOW warnings;
```

```bash
MariaDB [(none)]> CREATE DATABASE IF NOT EXISTS platzi_operation;
Query OK, 0 rows affected, 1 warning (0,000 sec)

MariaDB [(none)]> SHOW warnings;
+-------+------+-----------------------------------------------------------+
| Level | Code | Message                                                   |
+-------+------+-----------------------------------------------------------+
| Note  | 1007 | Can't create database 'platzi_operation'; database exists |
+-------+------+-----------------------------------------------------------+
1 row in set (0,000 sec)

MariaDB [(none)]> 
```


## Crear nuestra primera tabla

- Recordar que cada tabla necesita un ID y para ello se utiliza un entero. 
```sql
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    author_id INTEGER UNSIGNED,
    title VARCHAR(100) NOT NULL,
    year INTEGER UNSIGNED NOT NULL DEFAULT 1990,
    lenguage VARCHAR(2) NOT NULL DEFAULT 'es' COMMENT 'ISO 639-1  lengaufe',
    cover_url VARCHAR(500),
    price DOUBLE(6,2) NOT NULL DEFAULT 10.0,
    sellable TINYINT(1) NOT NULL DEFAULT 1,
    copies INTEGER NOT NULL DEFAULT 1,
    description TEXT
);
```
```sql
CREATE TABLE IF NOT EXISTS authors (
    author_id INTEGER UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    nationality VARCHAR(3)
);
```

```sql
MariaDB [platzi_operation]> CREATE TABLE IF NOT EXISTS books (
    ->     book_id INTEGER UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    ->     author_id INTEGER UNSIGNED,
    ->     title VARCHAR(100) NOT NULL,
    ->     year INTEGER UNSIGNED NOT NULL DEFAULT 1990,
    ->     lenguage VARCHAR(2) NOT NULL DEFAULT 'es' COMMENT 'ISO 639-1  lengaufe',
    ->     cover_url VARCHAR(500),
    ->     price DOUBLE(6,2) NOT NULL DEFAULT 10.0,
    ->     sellable TINYINT(1) NOT NULL DEFAULT 1,
    ->     copies INTEGER NOT NULL DEFAULT 1,
    ->     description TEXT
    -> );
Query OK, 0 rows affected (0,034 sec)

MariaDB [platzi_operation]> CREATE TABLE IF NOT EXISTS author (
    ->     author_id INTEGER UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    ->     name VARCHAR(100) NOT NULL,
    ->     nationality VARCHAR(3)
    -> );
Query OK, 0 rows affected (0,024 sec)

MariaDB [platzi_operation]> show tables;
+----------------------------+
| Tables_in_platzi_operation |
+----------------------------+
| author                     |
| books                      |
+----------------------------+
2 rows in set (0,000 sec)

MariaDB [platzi_operation]> 
```

- Para borrar una tabla se utiliza el comando `drop table`
```sql
drop table [Nombre de la tabla]
```
- Con el comando `describe [Nombre de la tabla]`
```sql
$ describe [Nombre de la tabla]

MariaDB [platzi_operation]> describe author;
+-------------+------------------+------+-----+---------+----------------+
| Field       | Type             | Null | Key | Default | Extra          |
+-------------+------------------+------+-----+---------+----------------+
| author_id   | int(10) unsigned | NO   | PRI | NULL    | auto_increment |
| name        | varchar(100)     | NO   |     | NULL    |                |
| nationality | varchar(3)       | YES  |     | NULL    |                |
+-------------+------------------+------+-----+---------+----------------+
3 rows in set (0,001 sec)
```

- Con el comando `desc [Nombre de la tabla]` le muestra todas las columnas que necesita la base de datos
```sql
$ desc [Nombre de la tabla]

MariaDB [platzi_operation]> desc author;
+-------------+------------------+------+-----+---------+----------------+
| Field       | Type             | Null | Key | Default | Extra          |
+-------------+------------------+------+-----+---------+----------------+
| author_id   | int(10) unsigned | NO   | PRI | NULL    | auto_increment |
| name        | varchar(100)     | NO   |     | NULL    |                |
| nationality | varchar(3)       | YES  |     | NULL    |                |
+-------------+------------------+------+-----+---------+----------------+
3 rows in set (0,001 sec)

MariaDB [platzi_operation]> desc books;
+-------------+------------------+------+-----+---------+----------------+
| Field       | Type             | Null | Key | Default | Extra          |
+-------------+------------------+------+-----+---------+----------------+
| book_id     | int(10) unsigned | NO   | PRI | NULL    | auto_increment |
| author_id   | int(10) unsigned | YES  |     | NULL    |                |
| title       | varchar(100)     | NO   |     | NULL    |                |
| year        | int(10) unsigned | NO   |     | 1990    |                |
| lenguage    | varchar(2)       | NO   |     | es      |                |
| cover_url   | varchar(500)     | YES  |     | NULL    |                |
| price       | double(6,2)      | NO   |     | 10.00   |                |
| sellable    | tinyint(1)       | NO   |     | 1       |                |
| copies      | int(11)          | NO   |     | 1       |                |
| description | text             | YES  |     | NULL    |                |
+-------------+------------------+------+-----+---------+----------------+
10 rows in set (0,001 sec)

MariaDB [platzi_operation]> 
```


- describe todo el contenido de la tabla, como: field, Type data, collaction, Null, key, Extra, Privileges, coment*/
```sql
$ SHOW FULL COLUMNS FROM books;

MariaDB [platzi_operation]> SHOW FULL COLUMNS FROM books;
+-------------+------------------+--------------------+------+-----+---------+----------------+---------------------------------+---------------------+
| Field       | Type             | Collation          | Null | Key | Default | Extra          | Privileges                      | Comment             |
+-------------+------------------+--------------------+------+-----+---------+----------------+---------------------------------+---------------------+
| book_id     | int(10) unsigned | NULL               | NO   | PRI | NULL    | auto_increment | select,insert,update,references |                     |
| author_id   | int(10) unsigned | NULL               | YES  |     | NULL    |                | select,insert,update,references |                     |
| title       | varchar(100)     | utf8mb4_unicode_ci | NO   |     | NULL    |                | select,insert,update,references |                     |
| year        | int(10) unsigned | NULL               | NO   |     | 1990    |                | select,insert,update,references |                     |
| lenguage    | varchar(2)       | utf8mb4_unicode_ci | NO   |     | es      |                | select,insert,update,references | ISO 639-1  lengaufe |
| cover_url   | varchar(500)     | utf8mb4_unicode_ci | YES  |     | NULL    |                | select,insert,update,references |                     |
| price       | double(6,2)      | NULL               | NO   |     | 10.00   |                | select,insert,update,references |                     |
| sellable    | tinyint(1)       | NULL               | NO   |     | 1       |                | select,insert,update,references |                     |
| copies      | int(11)          | NULL               | NO   |     | 1       |                | select,insert,update,references |                     |
| description | text             | utf8mb4_unicode_ci | YES  |     | NULL    |                | select,insert,update,references |                     |
+-------------+------------------+--------------------+------+-----+---------+----------------+---------------------------------+---------------------+
10 rows in set (0,001 sec)

```


```sql
CREATE TABLE clients (
    client_id INTEGER UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    `name`  VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    birthdate DATETIME,
    gender ENUM('M', 'F', 'ND') NOT NULL,
    activate  TINYINT(1) NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );

```
### Explciacion de la tabla clients

- **CREATE TABLE**: Comando utilizado para crear una nueva tabla en una base de datos.

- **clients**: Nombre de la tabla que estamos creando.

- **client_id**: Nombre de la columna que servirá como identificador único para cada cliente.

- **INTEGER UNSIGNED**: Tipo de datos que indica un número entero que no puede ser negativo.

- **PRIMARY KEY**: Especifica que la columna `client_id` es la clave primaria de la tabla, es decir, un valor único que identifica de manera única cada fila en la tabla.

- **AUTO_INCREMENT**: Indica que el valor de la columna `client_id` se incrementa automáticamente para cada nueva fila insertada en la tabla.

- **`name`**: Nombre de la columna que almacenará el nombre del cliente. Se usa comillas invertidas para encerrar el nombre debido a que "name" es una palabra reservada en MySQL.

- **VARCHAR(50)**: Tipo de datos que indica una cadena de caracteres de longitud variable con una longitud máxima de 50 caracteres.

- **NOT NULL**: Restricción que indica que el valor en esta columna no puede ser nulo, es decir, debe contener datos.

- **email**: Nombre de la columna que almacenará la dirección de correo electrónico del cliente.

- **UNIQUE**: Restricción que asegura que cada valor en la columna `email` sea único, es decir, no se puede repetir en la tabla.

- **birthdate**: Nombre de la columna que almacenará la fecha de nacimiento del cliente.

- **DATETIME**: Tipo de datos que almacena valores de fecha y hora en el formato 'YYYY-MM-DD HH:MM:SS'.

- **gender**: Nombre de la columna que almacenará el género del cliente.

- **ENUM('M', 'F', 'ND')**: Tipo de datos que permite especificar un conjunto de valores posibles para la columna. En este caso, 'M' representa masculino, 'F' femenino y 'ND' no definido.

- **activate**: Nombre de la columna que almacenará el estado de activación del cliente.

- **TINYINT(1)**: Tipo de datos que almacena números enteros pequeños. En este caso, se usa para almacenar valores binarios (0 o 1) que representan estados de activación.

- **DEFAULT 1**: Valor predeterminado que se asigna a la columna `activate` si no se proporciona ningún valor durante la inserción de datos.

- **created_at**: Nombre de la columna que almacenará la fecha y hora en que se creó el registro del cliente.

- **updated_at**: Nombre de la columna que almacenará la fecha y hora de la última actualización del registro del cliente.

- **TIMESTAMP**: Tipo de datos que almacena valores de fecha y hora. Se utiliza para registrar la fecha y hora de creación y actualización de registros.

- **CURRENT_TIMESTAMP**: Valor que se asigna automáticamente a las columnas `created_at` y `updated_at` cuando se inserta o actualiza un registro, respectivamente.

- **ON UPDATE CURRENT_TIMESTAMP**: Regla que indica que la columna `updated_at` se actualizará automáticamente con la fecha y hora actuales cada vez que se modifique una fila en la tabla.

```sql
    CREATE TABLE IF NOT EXISTS operations (
    operation_id INTEGER UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    book_id INTEGER UNSIGNED NOT NULL,
    client_id INTEGER UNSIGNED NOT NULL,
    type ENUM('sele', 'loan', 'return') NOT NULL,
    create_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    finished TINYINT(1) NOT NULL
    );

```

- Formas en las que se insertan valores a una tabla:

Primera forma
```sql
INSERT INTO authors(author_id, name, nationality) VALUES('', 'Juan Rulfo', 'MEX');
```
Segunda forma
```sql
INSERT INTO authors(name, nationality) VALUES('Gabriel Garcia Márquez', 'COL');
```

Tercera forma
```sql
INSERT INTO authors VALUES('Juan Gabriel Vasquez', 'COL');

```

- Insertar al mismo tiempo varias columnas:

```sql
INSERT INTO authors(name, nationality) 
VALUES('Juan Gabriel Vasquez', 'COL'),
    ('Julio Cortázar', 'ARG'),
    ('Isabel Allende', 'CHI'),
    ('Octavio Paz', 'MEX'),
    ('Juan Carlos Onetti', 'URU');


```

```sql
INSERT INTO clients (client_id, name, email, birthdate,gender, activate)
VALUES 
(1,'Maria Dolores Gomez','Maria Dolores.95983222J@random.names','1971-06-06','F',1),
(2,'Adrian Fernandez','Adrian.55818851J@random.names','1970-04-09','M',1),
(3,'Maria Luisa Marin','Maria Luisa.83726282A@random.names','1957-07-30','F',1),
(4,'Pedro Sanchez','Pedro.78522059J@random.names','1992-01-31','M',1);

```

- Para coger uno de los datos y presentarlo se ejecuta el siguiente comando:

```sql
select * from clients where client_id = 4\G
```
- El dato es presentado de esta manera
```bash
MariaDB [platzi_operation]> select * from clients where client_id = 4\G;
*************************** 1. row ***************************
 client_id: 4
      name: Pedro Sanchez
     email: Pedro.78522059J@random.names
 birthdate: 1992-01-31 00:00:00
    gender: M
  activate: 1
created_at: 2024-02-24 12:38:28
updated_at: 2024-02-24 12:38:28
1 row in set (0,001 sec)

ERROR: No query specified

```

Y asi con cada uno de las columnas. Por el momento pues, ire conociendo mas comandos que puede que hagan mejor esta tarea de las búsquedas. 

```sql
select * from clients where gender = 'M'\G;
```


Ingresar un libre de un author que ya esta en la base de datos 

```sql
/* Insertamos a mano */
INSERT INTO books(title, author_id) VALUES('El laberinto de la Soledad', 6);

/* Insertamos con select */
INSERT INTO books(title, author_id, `year`)
VALUES('Vuelta al Laberinto de la Soledad', 
(SELECT author_id 
FROM authors 
WHERE name = 'Octavio Paz'
LIMIT 1), 1960);
```


```sql
INSERT INTO transactions(transaction_id, book_id, client_id, type, finished) VALUES(NULL, 3, 7, 'lend', 0);

INSERT INTO transactions(transaction_id, book_id, client_id, type, finished) VALUES(NULL, 4, 8, 'sell', 0);

INSERT INTO transactions(transaction_id, book_id, client_id, type, finished) VALUES(NULL, 6, 3, 'sell', 1);

INSERT INTO transactions(transaction_id, book_id, client_id, type, finished) VALUES(NULL, 5, 2, 'lend', 1);

INSERT INTO transactions(transaction_id, book_id, client_id, type, finished) VALUES(NULL, 10, 4, 'lend', 0);

INSERT INTO transactions(transaction_id, book_id, client_id, type, finished) VALUES(NULL, 12, 9, 'sell', 1);>
```

- Para mandar todo un archvio configurado para crear las tablas y los datos, pero en una base de datos no existente; Esta tanbien se crea con el archivo:

```sql
sudo mysql -u root -p < all.sql
```

- En caso de que la base de datos ya este dentor del mysql pero no tenga nada de informacion:

```sql
sudo mysql -u root -p -D [base de datos que existe] < all.sql
```


## Select

- Este comando es el que nos muetsra la tabla completa de la base de datos.
```sql
select * from [nombre_tabla]
```

- Si quiere seleccionar una collumna especifica de la tabla lo hago de la siguiente manera:
```sql
select [nombre_columna] from [nombre_tabla]

MariaDB [pruebaplatzi]> select `name` from clients;
```

- Y puedo llamar las columnas que necesite:
```sql
select [nombre_columna_1], [nombre_columna_2] from [nombre_tabla]

MariaDB [pruebaplatzi]> select `name`, gender, birthdate from clients;
```
- para agregar una condicion a la busqueda de limite:
```sql
select [nombre_columna_1], [nombre_columna_2] from [nombre_tabla] limit 10

MariaDB [pruebaplatzi]> select `name`, gender, birthdate from clients limit 10
MariaDB [pruebaplatzi]> select `name`, gender, birthdate from clients limit 10
    -> ;
+---------------------+--------+------------+
| name                | gender | birthdate  |
+---------------------+--------+------------+
| Maria Dolores Gomez | F      | 1971-06-06 |
| Adrian Fernandez    | M      | 1970-04-09 |
| Maria Luisa Marin   | F      | 1957-07-30 |
| Pedro Sanchez       | M      | 1992-01-31 |
| Pablo Saavedra      | M      | 1960-07-21 |
| Marta Carrillo      | F      | 1981-06-15 |
| Javier Barrio       | M      | 1971-04-24 |
| Milagros Garcia     | F      | 1964-12-05 |
| Carlos Quiros       | M      | 1954-08-28 |
| Carmen De la Torre  | F      | 1966-05-14 |
+---------------------+--------+------------+
10 rows in set (0,000 sec)

```

- Empezar a condicionar la busqueda
```sql
SELECT `name`, birthdate, gender from clients WHERE gender = 'M'
```

### Utilizacion de funciones

- Traer solo el ano en la que nacio cada persona
```sql
SELECT year(birthdate), FROM clients 
```

- Una funcion que te nuestra fecha y la hora de hoy 
```sql
SELECT now() 
```

- Tambien se puede asocialr funciones
```sql
SELECT YEAR(NOW())
```

- Mas combinaciones, como por ejemplo, hacer calculos por fecha. Por ejemplo esta, resta la fecha de hoy co el birthdate para sacar la edad:
```sql
SELECT YEAR(NOW()) - YEAR(birthdate) FROM clients
```

- Para agragare a a query anterior e nombre de a persona, se hace de a siguiente manera:
```sql
SELECT `name`, YEAR(NOW()) - YEAR(birthdate) FROM clients
```

- Otra funcion de comparacion es like. En particula, like es una funcion de cercania de textos.
```sql
SELECT * FROM clients WHERE `name` LIKE '%Saavedra%'

MariaDB [pruebaplatzi]> SELECT * FROM clients WHERE `name` LIKE '%Saave%';
+-----------+----------------+------------------------------+------------+--------+--------+---------------------+
| client_id | name           | email                        | birthdate  | gender | active | created_at          |
+-----------+----------------+------------------------------+------------+--------+--------+---------------------+
|         5 | Pablo Saavedra | Pablo.93733268B@random.names | 1960-07-21 | M      |      1 | 2018-04-09 16:51:30 |
+-----------+----------------+------------------------------+------------+--------+--------+---------------------+
1 row in set (0,001 sec)
```
% este simbo lo queire decir dentro de la expresion, que no importa que haya adelante en el primero y despues en el segundo $

En este query compuesto se le pone un alias a la edad
```sql
SELECT name, email, YEAR(NOW()) - YEAR(birthdate) AS edad, gender FROM clients WHERE gender = 'F' AND name LIKE '%Lop%'


MariaDB [pruebaplatzi]> SELECT name, email, YEAR(NOW()) - YEAR(birthdate) AS edad, gender FROM clients WHERE gender = 'F' AND name LIKE '%Lop%';
+-------------------+------------------------------------+------+--------+
| name              | email                              | edad | gender |
+-------------------+------------------------------------+------+--------+
| Juana Maria Lopez | Juana Maria.51072683X@random.names |   34 | F      |
| Carmen Lopez      | Carmen.09399409E@random.names      |   37 | F      |
+-------------------+------------------------------------+------+--------+
2 rows in set (0,001 sec)
```

### Relaciones y cruces entre tablas

- Para contar vlaores uso el comanod count(*)
```sql
SELECT COUNT(*) FROM books
```

Dos formas de hacer la misma condicion
```sql
SELECT * SELECT * FROM authors WHERE author_id BETWEEN 1 AND 5;

SELECT * SELECT * FROM authors WHERE author_id > 0 AND author_id <=5;

```

- Aca ya se empieza a cruzar tablas
```sql
SELECT * FROM books WHERE author_id BETWEEN 1 and 5;
```

### Join

```sql
SELECT b.book_id, a.name, b.title FROM books as b
JOIN authors AS a
    on a.author_id = b.author_id
WHERE b.author_id BETWEEN 1 and 5;
```

- Se pueden unir todas las tablas que se quiera
```sql
select c.name, t.type, b.title, a.name from transactions as t
join books as b
    on b.book_id = t.book_id
join authors as a
    on b.author_id = a.author_id
join clients as c
    on t.client_id = c.client_id
where c.gender = 'M' and t.type = 'sell';
```
- otro ejemplo pero agregandole otro condicional con `in`
- Se pueden unir todas las tablas que se quiera
```sql
select c.name, t.type, b.title, a.name from transactions as t
join books as b
    on b.book_id = t.book_id
join authors as a
    on b.author_id = a.author_id
join clients as c
    on t.client_id = c.client_id
where c.gender = 'M' and t.type in ('sell', 'lend');

```

- El order by sirve para definir el orden que se quiere utilizar.

```sql
select a.author_id, a.name, a.nationality, b.title
from authors as a join
books as b
    on b.author_id = a.author_id
where a.author_id between 1 and 5
order by a.name [desc o asc];
```

- La diferancia entre el join y el left join, es que el left join trae toido, incluso si ese autor no tiene un libro dentro de la tabla de libros.

```sql
select a.author_id, a.name, a.nationality, b.title
from authors as a left join
books as b
    on b.author_id = a.author_id
where a.author_id between 1 and 5
order by a.name [desc o asc];
```


## Funciones de colunna 
### Uso de count


```sql
select a.author_id, a.name, a.nationality, COUNT(b.book_id)
from authors as a join
books as b
    on b.author_id = a.author_id
where a.author_id between 1 and 5
GROUP BY a.author_id
order by a.name desc ;

+-----------+--------------------+-------------+------------------+
| author_id | name               | nationality | COUNT(b.book_id) |
+-----------+--------------------+-------------+------------------+
|         1 | Sam Altman         | USA         |                2 |
|         5 | Juan Rulfo         | MEX         |                1 |
|         3 | Arthur Conan Doyle | GBR         |                3 |
+-----------+--------------------+-------------+------------------+

```
- La diferencia entre contar cuando se utiliza el join y el left join, es que junto con le lesf jpin tiene en cuenta los valores en cero. Es decir, si dentro de la tabla de libros, no hay ninguyno para ciertos autores, su valor en count se mostrará en cero.  como aparece en la tabla resultado.

```sql
select a.author_id, a.name, a.nationality, COUNT(b.book_id)
from authors as a left join
books as b
    on b.author_id = a.author_id
where a.author_id between 1 and 5
GROUP BY a.author_id
order by a.name desc ;


+-----------+--------------------+-------------+------------------+
| author_id | name               | nationality | COUNT(b.book_id) |
+-----------+--------------------+-------------+------------------+
|         1 | Sam Altman         | USA         |                2 |
|         5 | Juan Rulfo         | MEX         |                1 |
|         2 | Freddy Vega        | COL         |                0 |
|         4 | Chuck Palahniuk    | USA         |                0 |
|         3 | Arthur Conan Doyle | GBR         |                3 |
+-----------+--------------------+-------------+------------------+
5 rows in set (0,001 sec)

```

### 1. Inner Join

Esta es la forma mas fácil de seleccionar información de diferentes tablas, es tal vez la que mas usas a diario en tu trabajo con bases de datos. Esta union retorna todas las filas de la tabla A que coinciden en la tabla B. Es decir aquellas que están en la tabla A Y en la tabla B, si lo vemos en conjuntos la intersección entre la tabla A y la B.

![Alt text](image.png)

Esto lo podemos implementar de esta forma cuando estemos escribiendo las consultas:

```sql
SELECT <columna_1> , <columna_2>,  <columna_3> ... <columna_n> 
FROM Tabla_A A
INNER JOIN Tabla_B B
ON A.pk = B.pk
```

### 2. Left Join

Esta consulta retorna todas las filas que están en la tabla A y ademas si hay coincidencias de filas en la tabla B también va a traer esas filas.

![Alt text](image-1.png)

Esto lo podemos implementar de esta forma cuando estemos escribiendo las consultas:

```sql
SELECT <columna_1> , <columna_2>,  <columna_3> ... <columna_n> 
FROM Tabla_A A
LEFT JOIN Tabla_B B
ON A.pk = B.pk
```

### 3. Right Join

Esta consulta retorna todas las filas de la tabla B y ademas si hay filas en la tabla A que coinciden también va a traer estas filas de la tabla A.

![Alt text](image-2.png)

Esto lo podemos implementar de esta forma cuando estemos escribiendo las consultas:

```sql
SELECT <columna_1> , <columna_2>,  <columna_3> ... <columna_n>
FROM Tabla_A A
RIGHT JOIN Tabla_B B
ON A.pk = B.pk
```

### 4. Outer Join

Este join retorna TODAS las filas de las dos tablas. Hace la union entre las filas que coinciden entre la tabla A y la tabla B.

![Alt text](image-3.png)

Esto lo podemos implementar de esta forma cuando estemos escribiendo las consultas:

```sql
SELECT <columna_1> , <columna_2>,  <columna_3> ... <columna_n>
FROM Tabla_A A
FULL OUTER JOIN Tabla_B B
ON A.pk = B.pk
```

### 5. Left excluding join

Esta consulta retorna todas las filas de la tabla de la izquierda, es decir la tabla A que no tienen ninguna coincidencia con la tabla de la derecha, es decir la tabla B.

![Alt text](image-4.png)

Esto lo podemos implementar de esta forma cuando estemos escribiendo las consultas:

```sql
SELECT <columna_1> , <columna_2>,  <columna_3> ... <columna_n>
FROM Tabla_A A
LEFT JOIN Tabla_B B
ON A.pk = B.pk
WHERE B.pk IS NULL

```

### 6. Right Excluding join

Esta consulta retorna todas las filas de la tabla de la derecha, es decir la tabla B que no tienen coincidencias en la tabla de la izquierda, es decir la tabla A.

![Alt text](image-5.png)

Esto lo podemos implementar de esta forma cuando estemos escribiendo las consultas:

```sql
SELECT <columna_1> , <columna_2>,  <columna_3> ... <columna_n>
FROM Tabla_A A
RIGHT JOIN Tabla_B B
ON A.pk = B.pk
WHERE A.pk IS NULL

```

### 7. Outer excluding join

Esta consulta retorna todas las filas de la tabla de la izquierda, tabla A, y todas las filas de la tabla de la derecha, tabla B que no coinciden.

![Alt text](image-6.png)

Esto lo podemos implementar de esta forma cuando estemos escribiendo las consultas:

```sql
SELECT <select_list>
FROM Table_A A
FULL OUTER JOIN Table_B B
ON A.Key = B.Key
WHERE A.Key IS NULL OR B.Key IS NULL
```

## Traducción de preguntas en lenguaje sql

### 1. ¿Qué nacionalidades?

```sql
SELECT DISTINCT nationality from authors;

```

- Con este comando se cuenta la frecuencia por nacionalidad
```sql
select nationality, COUNT(nationality) as c_nationality
from authors
group by nationality;
```


### 2. ¿Cuantos escritores hay para cada nacionalidad?

```sql
SELECT nationality, COUNT(author_id) AS c_authors
FROM authors
GROUP BY nationality
ORDER BY c_authors DESC, nationality ASC;
```


- Este comando selecciona de la base de la tabla de authores quellos cuya nacionalidad sea USA y esta información la acompaña con los nombre de los titulos que han escrito. 
```sql
SELECT a.name, b.title
from authors as a join books as b
    on a.author_id = b.author_id
where a.nationality = 'USA'
ORDER BY a.name asc;
```

- Comando para seleccionar aquellos autores cuya nacionalidad es NULL
```sql
SELECT a.name, b.title, a.nationality
from authors as a join books as b
    on a.author_id = b.author_id
where a.nationality is NULL
ORDER BY a.name asc;
```

- Comando para seleccionar aquellos autores cuya nacionalidad es no NULL
```sql
SELECT a.name, b.title, a.nationality
from authors as a join books as b
    on a.author_id = b.author_id
where a.nationality is not NULL
ORDER BY a.name asc;
```

- Comando para seleccionar aquellos autores cuya nacionalidad no sea diferente a un pais en especifico o varios paises u que tambien sean no null.
```sql
SELECT a.name, b.title, a.nationality
from authors as a join books as b
    on a.author_id = b.author_id
where a.nationality is not NULL
and a.nationality not in('RUS', 'USA')
ORDER BY a.name asc;
```

### Usao de operaciones matematicas


### 4. Cuales el promedio y lka desviación estandar del precio de libros


```sql
select nationality,
    COUNT(book_id) as libros,
    AVG(price) as prom,
    STDDEV(price) as std
from books as b
join authors as a
    on a.author_id = b.author_id
GROUP BY nationality
ORDER BY libros desc;
```

### 5. Idem, pero por nacionalidad

### 6. Cual es el precion maximo y minimo de un libro
```sql
SELECT MAX(price), MIN(price) from books;
```
- Ahora hamolo pero por paises

```sql
SELECT a.nationality, MAX(price), MIN(price)
from books as b join
authors as a
    on a.author_id = b.author_id
GROUP BY nationality;
```
### 7. ¿Como quedaría el reporte de prestamos?

```sql
SELECT c.name as client, t.type, b.title, a.name as author, a.nationality, t.created_at
FROM transactions AS t
LEFT JOIN clients As c
    ON c.client_id = t.client_id
LEFT JOIN books As b
    ON b.book_id = t.book_id
LEFT JOIN authors As a
    ON b.author_id = a.author_id
ORDER BY t.created_at;
```

- Ahora hagamos esto mismo pero concatenando el autor co la nacionalidad en una misma columna.

```sql
SELECT c.name as client, t.type, b.title,
CONCAT(a.name, " (", a.nationality, ")") 
    as author, t.created_at
FROM transactions AS t
LEFT JOIN clients As c
    ON c.client_id = t.client_id
LEFT JOIN books As b
    ON b.book_id = t.book_id
LEFT JOIN authors As a
    ON b.author_id = a.author_id
ORDER BY t.created_at;
```

### Calculo con fechas

```sql
SELECT c.name as client, t.type, b.title,
CONCAT(a.name, " (", a.nationality, ")") 
    as author,
    TO_DAYS(NOW()) - TO_DAYS(t.created_at) as Ago
FROM transactions AS t
LEFT JOIN clients As c
    ON c.client_id = t.client_id
LEFT JOIN books As b
    ON b.book_id = t.book_id
LEFT JOIN authors As a
    ON b.author_id = a.author_id
ORDER BY t.created_at;
```


### Comandos UPDATE Y DELETE

- Este comando es para eliminar o varias lineas de la tabla
```sql
DELETE FROM authors WHERE author_id = 47;
```

- Este comando es para actualizar uno o varios valores en una tabla. El limit 1 es opcional pero se indica cuando es posible que existan valores repetidos solo borre uno.
```sql
UPDATE clients SET active = 0 where client_id = 5 limit 1;
```
- Actualizar varios elementos
```sql
UPDATE clients SET active = 0 where client_id in (1,3,9)
```

## Super Querys

- Funcion sun()
```sql
select sum(price) from books where sellable = 1;
```
- Usos de la funcion sum()
```sql
select sum(price*copies) from books where sellable = 1;
```

```sql
select sellable, sum(price*copies) from books group by sellable;
```
### Condicional if

```sql
select count(book_id), sum(if(year < 1950, 1, 0)) as "<1950" from books;

select count(book_id) as total_books, sum(if(year < 1950, 1, 0)) as "<1950" from books;

select count(book_id) as total_books, sum(if(year < 1950, 1, 0)) as "<1950", sum(if(year > 1950, 1, 0)) as ">1950" from books;
```
- Caomando complejo

```sql
select nationality, count(book_id),
    sum(if(year < 1950, 1, 0)) as "<1950",
    sum(if(year >= 1950 and year < 1990, 1, 0)) as "<1990",
    sum(if(year >= 1990 and year < 2000, 1, 0)) as "<2000",
    sum(if(year >= 2000, 1, 0)) as "Hoy"
from books as b
join authors as a
    on a.author_id = b.author_id
where
    a.nationality is not null
group by nationality;

+-------------+----------------+-------+-------+-------+------+
| nationality | count(book_id) | <1950 | <1990 | <2000 | Hoy  |
+-------------+----------------+-------+-------+-------+------+
| AUS         |              2 |     2 |     0 |     0 |    0 |
| AUT         |              4 |     4 |     0 |     0 |    0 |
| DEU         |              1 |     1 |     0 |     0 |    0 |
| ENG         |             16 |    16 |     0 |     0 |    0 |
| ESP         |              1 |     1 |     0 |     0 |    0 |
| FRA         |              3 |     3 |     0 |     0 |    0 |
| GBR         |              3 |     3 |     0 |     0 |    0 |
| IND         |              8 |     8 |     0 |     0 |    0 |
| JAP         |              1 |     1 |     0 |     0 |    0 |
| MEX         |              1 |     0 |     1 |     0 |    0 |
| RUS         |              9 |     9 |     0 |     0 |    0 |
| SWE         |             11 |     3 |     0 |     8 |    0 |
| USA         |             28 |    26 |     0 |     0 |    2 |
+-------------+----------------+-------+-------+-------+------+
13 rows in set (0,002 sec)


    
```




