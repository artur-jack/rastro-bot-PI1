const express = require('express');
const bodyParser = require('body-parser');
const sqlite3 = require('sqlite3').verbose();
const asyncHandler = require('express-async-handler');

const app = express();
const port = 3000;

// Middleware para fazer parse do corpo das requisições como JSON
app.use(bodyParser.json());

// Middleware para registrar a hora da requisição
app.use((req, res, next) => {
  const requestTime = new Date().toISOString();
  console.log(`Requisição recebida em: ${requestTime}`);
  req.requestTime = requestTime; // Adiciona o horário da requisição ao objeto req
  next();
});

// Configuração do banco de dados SQLite
let db;

// Função para configurar o banco de dados SQLite
const setupDatabase = () => {
  return new Promise((resolve, reject) => {
    db = new sqlite3.Database('./database.db', (err) => {
      if (err) {
        reject(err);
      } else {
        db.run(`CREATE TABLE IF NOT EXISTS readings (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          sensor_esquerdo INTEGER,
          sensor_direito INTEGER,
          velocidade REAL,
          distancia REAL,
          timestamp TEXT
        )`, (err) => {
          if (err) {
            reject(err);
          } else {
            console.log('Conectado ao banco de dados SQLite');
            resolve();
          }
        });
      }
    });
  });
};

// Função para inserir dados no banco de dados
const insertData = (data) => {
  const { sensor_esquerdo, sensor_direito, velocidade, distancia, timestamp } = data;
  return new Promise((resolve, reject) => {
    db.run(`INSERT INTO readings (sensor_esquerdo, sensor_direito, velocidade, distancia, timestamp)
            VALUES (?, ?, ?, ?, ?)`,
            [sensor_esquerdo, sensor_direito, velocidade, distancia, timestamp],
            (err) => {
              if (err) {
                console.error('Erro ao inserir dados:', err.message);
                reject(err);
              } else {
                console.log('Dados inseridos com sucesso no banco de dados');
                resolve();
              }
            });
  });
};

// Rota para receber os dados do dispositivo ESP
app.post('/api/data', asyncHandler(async (req, res) => {
  const data = req.body; // Recebe o array de objetos JSON enviado pelo ESP32

  // Envie uma resposta de sucesso imediatamente
  res.status(200).json({ message: 'Dados recebidos, processamento em andamento!' });

  let hasError = false;

  for (const item of data) {
    try {
      await insertData(item);
    } catch (err) {
      hasError = true;
    }
  }

  if (hasError) {
    console.error('Erro ao inserir alguns dados no banco de dados');
  }
}));

// Inicia o servidor após configurar o banco de dados
setupDatabase()
  .then(() => {
    app.listen(port, () => {
      console.log(`Servidor API rodando em http://localhost:${port}`);
    });
  })
  .catch((err) => {
    console.error('Erro ao configurar o banco de dados:', err.message);
  });
