CREATE DATABASE sistema_estudiantes;
USE sistema_estudiantes;

CREATE TABLE Estudiantes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cedula VARCHAR(20) NOT NULL UNIQUE,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    direccion_residencia VARCHAR(255),
    residencia POINT NOT NULL, -- Campo de coordenadas de residencia
    direccion_trabajo VARCHAR(255),
    trabajo POINT NOT NULL -- Campo de coordenadas de trabajo
);

INSERT INTO Estudiantes (cedula, nombres, apellidos, direccion_residencia, residencia, direccion_trabajo, trabajo)
VALUES ('101223021', 'Luis Santiago', 'Forero Heredia', 'Calle 10 # 20-30',
        ST_GeomFromText('POINT(4.614619420253344 -74.11109924686157)', 4326), 'Calle 100 # 50-60',
        ST_GeomFromText('POINT(4.632385881334712 -74.0808453905504)', 4326));
        
SELECT nombres, apellidos,
       ST_Distance_Sphere(residencia, trabajo) AS distancia_residencia_trabajo	
FROM Estudiantes
ORDER BY distancia_residencia_trabajo ASC;


CREATE VIEW VistaEstudiantesDistancia AS
SELECT id, cedula, nombres, apellidos, direccion_residencia, direccion_trabajo,
       ST_Distance_Sphere(residencia, trabajo) AS distancia_residencia_trabajo
FROM Estudiantes;

SELECT * FROM VistaEstudiantesDistancia ORDER BY distancia_residencia_trabajo ASC;

SELECT id, cedula, nombres, apellidos, direccion_residencia, ST_AsText(residencia) AS residencia,
       direccion_trabajo, ST_AsText(trabajo) AS trabajo
FROM Estudiantes;
