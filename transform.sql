-- 
-- Query snippets to use with metabase
-- 
-- 
-- Create dimension tables
CREATE TABLE data (
    data INTEGER PRIMARY KEY, -- YYYYMMDD for easy sorting
    ano INTEGER NOT NULL,
    trimestre INTEGER NOT NULL,
    mes INTEGER NOT NULL
);
INSERT OR IGNORE INTO data (
     data,
     ano,
     trimestre,
     mes
)
SELECT CAST(strftime(CAST(DataAtendimento AS DATE), '%Y%m%d') AS INTEGER) AS data,
        AnoAtendimento AS ano,
        TrimestreAtendimento AS trimestre,
        MesAtendimento AS mes
FROM atendimento ;


CREATE SEQUENCE local_id START 1;
CREATE TABLE local (
    local_id INTEGER PRIMARY KEY,
    uf VARCHAR(10) NOT NULL,
    regiao VARCHAR(50) NOT NULL,
);
INSERT OR IGNORE INTO local (
     uf,
     regiao
)
SELECT Uf,
       Regiao
FROM atendimento;


CREATE TABLE tipo_atendimento (
    tipo_id INTEGER PRIMARY KEY,
    descricao VARCHAR(1000) NOT NULL,
    id INTEGER NOT NULL,
);
INSERT OR IGNORE INTO tipo_atendimento (
     descricao,
     id
)
SELECT DescricaoTipoAtendimento AS descricao,
       CodigoTipoAtendimento AS id
FROM atendimento;

CREATE TABLE consumidor (
    id INTEGER PRIMARY KEY,
    sexo VARCHAR(10) NOT NULL,
    idade VARCHAR(15) NOT NULL,
    cep VARCHAR(20) NOT NULL
);
INSERT OR IGNORE INTO consumidor (
     sexo,
     idade,
     cep
)
SELECT SexoConsumidor AS sexo,
       FaixaEtariaConsumidor AS idade
       CEPConsumidor AS cep
FROM atendimento;


CREATE TABLE problema (
    descricao VARCHAR(1000) PRIMARY KEY,
    codigo INTEGER,
    grupo VARCHAR(1000) NOT NULL
);
INSERT OR IGNORE INTO problema (
     descricao,
     codigo,
     grupo
)
SELECT DescricaoProblema AS descricao,
       CodigoProblema AS codigo,
       GrupoProblema AS grupo
FROM atendimento
WHERE descricao != 'NULL' AND 
      codigo != 'NULL' AND
      grupo != 'NULL' ;


CREATE TABLE assunto (
    descricao VARCHAR(1000) NOT NULL,
    codigo INTEGER NOT NULL PRIMARY KEY,
    grupo VARCHAR(1000) NOT NULL
);
INSERT OR IGNORE INTO assunto (
     descricao,
     codigo,
     grupo
)
SELECT DescricaoAssunto AS descricao,
       CodigoAssunto AS codigo,
       GrupoAssunto AS grupo
FROM atendimento ;


-- Create fact table
CREATE TABLE facts (
     data INTEGER REFERENCES data(data),
     local INTEGER REFERENCES local(uf, regiao),
     tipo_atendimento INTEGER REFERENCES tipo_atendimento(descricao, id),
     consumidor INTEGER REFERENCES consumidor(cons_id),
     problema INTEGER REFERENCES problema(atend_id),
     assunto INTEGER REFERENCES assunto(atend_id),
     atendimento_id INTEGER PRIMARY KEY,
 );



