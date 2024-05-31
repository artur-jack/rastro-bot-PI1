# COMANDOS EM SQL PARA CRIAR O BANCO
```
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

create table DadosCorrida(
    idCorrida integer primary key,
    TempoColeta TIME,
    Distancia FLOAT,
    Velocidade FLOAT,
    Aceleracao FLOAT,
    Consumo FLOAT,
    FOREIGN KEY (idCorrida) REFERENCES Corrida(idCorrida) 
);
```
