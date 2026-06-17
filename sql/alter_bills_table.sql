--Mofidicion de tabla Bills con el siguiente comando:
ALTER TABLE Bills           
ADD telephone_number VARCHAR(20);
--Al correr el query anterior se agrega la columna telephone_number a la tabla Bills.

--Agregar columna employee_id a la tabla Bills
ALTER TABLE Bills
ADD employee_id INTEGER;
--Al correr el query anterior se agrega la columna employee_id a la tabla Bills.

--Ninguno de los dos queries correran realmente porque ya existen esas dos columnas en la tabla Bills, es solamente demostracion de como funcionan. 