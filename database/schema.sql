CREATE DATABASE IF NOT EXISTS guardianquake_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE guardianquake_db;

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario      INT AUTO_INCREMENT PRIMARY KEY,
    correo          VARCHAR(150) NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,
    tipo_cuenta     ENUM('FREE','PRO') NOT NULL DEFAULT 'FREE',
    fecha_registro  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS dispositivos (
    id_dispositivo          INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario              INT NOT NULL,
    modelo                  VARCHAR(100) NOT NULL,
    fabricante              VARCHAR(100) NOT NULL,
    so_version              VARCHAR(50),
    sensibilidad_recomendada DECIMAL(4,2) DEFAULT 5.00,
    fecha_registro          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_dispositivo_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS eventos_sismicos (
    id_evento           INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario           INT NOT NULL,
    id_dispositivo        INT NULL,
    fecha_hora            DATETIME NOT NULL,
    intensidad_aproximada DECIMAL(5,2) NOT NULL,
    duracion_ms           INT NOT NULL,
    sensibilidad_usada    TINYINT NOT NULL,
    fecha_registro        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_evento_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    CONSTRAINT fk_evento_dispositivo FOREIGN KEY (id_dispositivo) REFERENCES dispositivos(id_dispositivo)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS contenido_educativo (
    id_contenido        INT AUTO_INCREMENT PRIMARY KEY,
    titulo              VARCHAR(200) NOT NULL,
    cuerpo              TEXT NOT NULL,
    version             VARCHAR(20) NOT NULL DEFAULT '1.0',
    fecha_publicacion   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS suscripciones (
    id_suscripcion   INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario       INT NOT NULL,
    tipo             ENUM('PRO') NOT NULL DEFAULT 'PRO',
    fecha_inicio     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_fin        DATETIME NULL,
    estado           ENUM('ACTIVA','CANCELADA','EXPIRADA') NOT NULL DEFAULT 'ACTIVA',
    id_transaccion   VARCHAR(100) NOT NULL,
    plataforma       ENUM('GOOGLE_PLAY') NOT NULL DEFAULT 'GOOGLE_PLAY',
    CONSTRAINT fk_suscripcion_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS contactos_emergencia (
    id_contacto   INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario    INT NOT NULL,
    nombre        VARCHAR(150) NOT NULL,
    telefono      VARCHAR(20) NOT NULL,
    CONSTRAINT fk_contacto_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
) ENGINE=InnoDB;

-- Datos de prueba
INSERT INTO contenido_educativo (titulo, cuerpo, version) VALUES
('Percepcion de movimiento post-sismico',
 'Es normal sentir que el suelo sigue temblando minutos u horas despues de un sismo real; esto se debe a como el oido interno se adapta al movimiento. GuardianQuake te ayuda a verificar objetivamente si hay movimiento real usando el acelerometro del telefono.',
 '1.0'),
('Como calibrar la sensibilidad de tu dispositivo',
 'Cada modelo de telefono responde distinto al movimiento. Si recibes muchas alertas falsas, baja el nivel de sensibilidad; si no detecta movimientos leves, subelo gradualmente.',
 '1.0');

INSERT INTO usuarios (correo, password_hash, tipo_cuenta) VALUES
('demo@guardianquake.com', '$2b$12$placeholderplaceholderplaceholderplaceholder', 'FREE');

INSERT INTO dispositivos (id_usuario, modelo, fabricante, so_version, sensibilidad_recomendada) VALUES
(1, 'Galaxy A54', 'Samsung', 'Android 14', 5.50);
