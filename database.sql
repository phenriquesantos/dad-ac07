CREATE TABLE IF NOT EXIST teacher (
    id_teacher INTEGER PRIMARY KEY,
    nome VARCHAR(100)
);

CREATE TABLE IF NOT EXIST student (
    id_student INTEGER PRIMARY KEY,
    nome VARCHAR(100)
);

CREATE TABLE IF NOT EXIST subject (
    id_subject INTEGER PRIMARY KEY,
    nome VARCHAR(100),
    status INTEGER,
    plano_ensino VARCHAR(200),
    carga_horaria INTEGER,
    id_coordenador INTEGER NULL
        CONSTRAINT teacher REFERENCES teacher (id_teacher)
);