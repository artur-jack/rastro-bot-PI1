create database CarrinhoDB;

create table Corrida(
    idCorrida integer primary key autoincrement,
    Inicio DATETIME2,
    Fim DATETIME2,
    Estado VARCHAR(30),
    TempoTotal TIME,
    TrajetoTotal FLOAT,
    ConsumoMedio FLOAT,
    AceleracaoMedia FLOAT,
    VelocidadeMedia FLOAT    
);


