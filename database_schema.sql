-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS sgiru_db;
USE sgiru_db;

-- Tabla de Usuarios (Soporta HU-01: Login)
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    correo VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    rol ENUM('estudiante', 'docente', 'admin') DEFAULT 'estudiante',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Recursos/Espacios (Soporta HU-06 y HU-07: CRUD e Inventario)
CREATE TABLE recursos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo ENUM('laboratorio', 'aula', 'cubiculo') NOT NULL,
    req_software VARCHAR(100) DEFAULT 'ninguno',
    req_hardware VARCHAR(100) DEFAULT 'ninguno',
    estado ENUM('activo', 'inactivo', 'mantenimiento') DEFAULT 'activo'
);

-- Tabla de Reservas (Soporta HU-08: Cancelación y validación de fechas)
CREATE TABLE reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    recurso_id INT NOT NULL,
    fecha DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    estado ENUM('activa', 'cancelada', 'completada') DEFAULT 'activa',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (recurso_id) REFERENCES recursos(id) ON DELETE CASCADE
);

-- Insertar datos de prueba para que el prototipo tenga información real
INSERT INTO recursos (nombre, tipo, req_software, req_hardware) VALUES 
('Laboratorio de Redes 402', 'laboratorio', 'packet', 'switches'),
('Sala de Software 501', 'laboratorio', 'mysql', 'proyector'),
('Cubículo 3A', 'cubiculo', 'ninguno', 'ninguno');