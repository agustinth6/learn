-- ============================================================================
-- clinica_medica · base de practica para GROUP BY / HAVING / agregaciones
-- Datos exactos del material: «DATABASE clinica_medica — practica de todas
-- las consultas». 8 especialidades · 15 pacientes · 15 medicos · 30 turnos.
--
-- En MySQL Workbench: ejecuta este archivo completo y despues proba las
-- consultas del grupo de ejercicios.
-- En la terminal (sin MySQL):  python3 practica/run.py "SELECT ..."
-- ============================================================================

DROP DATABASE IF EXISTS clinica_medica;
CREATE DATABASE clinica_medica;
USE clinica_medica;

-- --------------------------------------------------------------- DDL -------
CREATE TABLE especialidades (
    id_especialidad INT AUTO_INCREMENT PRIMARY KEY,
    nombre_especialidad VARCHAR(50) NOT NULL
);

CREATE TABLE pacientes (
    id_paciente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    edad INT,
    ciudad VARCHAR(100)
);

CREATE TABLE medicos (
    id_medico INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    salario DECIMAL(10,2),
    id_especialidad INT,
    FOREIGN KEY (id_especialidad) REFERENCES especialidades(id_especialidad)
);

CREATE TABLE turnos (
    id_turno INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente INT,
    id_medico INT,
    fecha_turno DATE,
    motivo VARCHAR(100),
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente),
    FOREIGN KEY (id_medico) REFERENCES medicos(id_medico)
);

-- ---------------------------------------------------------------- DML ------
INSERT INTO especialidades (nombre_especialidad) VALUES
('Clínica General'), ('Cardiología'), ('Traumatología'), ('Dermatología'),
('Pediatría'), ('Neurología'), ('Ginecología'), ('Oftalmología');

INSERT INTO pacientes (nombre, apellido, edad, ciudad) VALUES
('María','González',35,'Buenos Aires'),
('Juan','Pérez',62,'Rosario'),
('Lucía','Ramírez',28,'Córdoba'),
('Diego','Fernández',45,'Mendoza'),
('Ana','Martínez',70,'Salta'),
('Pablo','Ríos',54,'La Plata'),
('Sofía','López',33,'Tucumán'),
('Carlos','Torres',58,'San Juan'),
('Laura','Silva',41,'Rosario'),
('Martín','Suárez',67,'Neuquén'),
('Valeria','Acosta',25,'Córdoba'),
('Jorge','Moreno',39,'Buenos Aires'),
('Natalia','Castro',51,'Mendoza'),
('Pedro','Benítez',73,'Rosario'),
('Camila','Sosa',30,'Salta');

INSERT INTO medicos (nombre, apellido, salario, id_especialidad) VALUES
('Luis','Moreno',420000,1),
('Carla','Ruiz',510000,2),
('Pedro','Luna',470000,3),
('Valeria','Sosa',430000,4),
('Andrés','Pérez',450000,5),
('Romina','Gómez',560000,6),
('Lucas','Benítez',495000,7),
('Marina','Castro',520000,8),
('Javier','Molina',410000,1),
('Camila','Ortega',540000,2),
('Tomás','Rivas',460000,3),
('Natalia','Herrera',435000,4),
('Sebastián','López',455000,5),
('Gabriela','Martínez',570000,6),
('Ricardo','Silva',530000,8);

-- cada turno cae en un dia distinto: 2025-10-01 .. 2025-10-30
INSERT INTO turnos (id_paciente, id_medico, fecha_turno, motivo) VALUES
(1,1,'2025-10-01','Control general'),
(2,2,'2025-10-02','Chequeo cardíaco'),
(3,3,'2025-10-03','Dolor de rodilla'),
(4,4,'2025-10-04','Problema de piel'),
(5,5,'2025-10-05','Control pediátrico'),
(6,6,'2025-10-06','Migrañas'),
(7,7,'2025-10-07','Control ginecológico'),
(8,8,'2025-10-08','Control visual'),
(9,1,'2025-10-09','Control general'),
(10,2,'2025-10-10','Hipertensión'),
(11,3,'2025-10-11','Fractura'),
(12,4,'2025-10-12','Dermatitis'),
(13,5,'2025-10-13','Control clínico'),
(14,6,'2025-10-14','Dolor de cabeza'),
(15,7,'2025-10-15','Consulta ginecológica'),
(1,8,'2025-10-16','Control visual'),
(2,1,'2025-10-17','Control general'),
(3,2,'2025-10-18','Chequeo cardíaco'),
(4,3,'2025-10-19','Traumatismo'),
(5,4,'2025-10-20','Alergia'),
(6,5,'2025-10-21','Control clínico'),
(7,6,'2025-10-22','Neurología'),
(8,7,'2025-10-23','Control anual'),
(9,8,'2025-10-24','Problemas de visión'),
(10,1,'2025-10-25','Control general'),
(11,2,'2025-10-26','Chequeo cardíaco'),
(12,3,'2025-10-27','Lesión deportiva'),
(13,4,'2025-10-28','Dermatitis'),
(14,5,'2025-10-29','Control médico'),
(15,6,'2025-10-30','Estudio neurológico');
