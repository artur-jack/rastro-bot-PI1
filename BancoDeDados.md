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

/* EXEMPLO DE INSERCAO
insert into Corrida(Inicio,Fim,Estado,TempoTotal,TrajetoTotal,ConsumoMedio,AceleracaoMedia,VelocidadeMedia) 
values('2024-05-30 09:30:00','2024-05-30 10:15:00','Finalizado','01:00:00',50.5,7.8,10.2,60.3);*/

create table DadosCorrida(
    id integer primary key autoincrement,
    TempoColeta TIME,
    Distancia FLOAT,
    Velocidade FLOAT,
    Aceleracao FLOAT,
    Consumo FLOAT
);

/* EXEMPLO DE INSERCAO
insert into DadosCorrida(TempoColeta,Distancia,Velocidade,Aceleracao,Consumo) values
('01:00:00',15.00,25.00,8.00,6.00)*/
```
