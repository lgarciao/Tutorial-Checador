DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS checks;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,                           -- ID del usuario
    username TEXT UNIQUE NOT NULL,                                  -- Usuario
    password TEXT NOT NULL,                                         -- Password de la cuenta
    email TEXT,                                                     -- Correo electrónico
    nombre TEXT NOT NULL,                                           -- Nombre del usuario
    ap_1 TEXT NOT NULL,                                             -- Primer apelido
    ap_2 TEXT,                                                      -- Segundo apellido
    fecha_creado DATETIME NOT NULL DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),      -- Fecha de creación
    userid_crea INTEGER,                                            -- ID de usuario que creó
    baja INTEGER NOT NULL DEFAULT 0                             -- Indica si el usuario está dado de baja
);

CREATE TABLE checks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,                           -- ID de la checada
    user_id INTEGER NOT NULL,                                       -- ID de usuario que checa
    checa_entrada DATETIME NOT NULL DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),     -- Fecha y hora de entrada
    checa_salida DATETIME,                                         -- Fecha y hora de salida
    baja INTEGER NOT NULL DEFAULT 0                             -- Inidca si la checada está dada de baja
);