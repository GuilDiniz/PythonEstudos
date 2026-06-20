# 📅 Plano de Estudos: 2 Semanas - Python, POO, MySQL e Docker

**Duração:** 14 dias | **Carga horária sugerida:** 2-3h/dia | **Objetivo:** Integração completa das 4 tecnologias

---

## 📍 **SEMANA 1: Fundamentos + Ferramentas**

### **DIA 1-2: Configuração do Ambiente + Docker Basics**

#### 🎯 Objetivos:
- Instalar Docker Desktop
- Entender conceitos básicos de containers
- Criar primeiro container

#### 📚 Conteúdo:

**Docker Desktop - Setup Inicial (1h)**
- Instalação em Windows/Mac/Linux
- Interface do Docker Desktop
- Verificar instalação: `docker --version`
- Conceitos: Imagens vs Containers
- Docker Hub

**Primeiro Container (1.5h)**
```bash
# Baixar imagem
docker pull ubuntu:latest

# Rodar container interativo
docker run -it ubuntu:latest /bin/bash

# Listar containers
docker ps -a

# Visualizar imagens
docker images
```

**Exercício Prático:**
```dockerfile
# Criar Dockerfile simples
FROM ubuntu:latest
RUN apt-get update && apt-get install -y python3
COPY . /app
WORKDIR /app
CMD ["python3", "--version"]
```

**Comandos essenciais:**
```bash
docker build -t meu-app:1.0 .
docker run meu-app:1.0
docker stop <container_id>
docker logs <container_id>
```

**Recursos:**
- [Docker Official Docs](https://docs.docker.com/)
- [Docker Desktop for Beginners](https://www.youtube.com/results?search_query=docker+desktop+tutorial)

---

### **DIA 3-4: MySQL Básico + Setup em Docker**

#### 🎯 Objetivos:
- Instalar MySQL via Docker
- Aprender SQL básico
- Conectar Python com MySQL

#### 📚 Conteúdo:

**MySQL com Docker (1.5h)**

```bash
# Criar container MySQL
docker run --name mysql-container \
  -e MYSQL_ROOT_PASSWORD=senha123 \
  -e MYSQL_DATABASE=estudos \
  -p 3306:3306 \
  -d mysql:8.0

# Conectar ao container
docker exec -it mysql-container mysql -u root -p

# Dentro do MySQL
CREATE DATABASE biblioteca;
USE biblioteca;

CREATE TABLE autores (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nome VARCHAR(100) NOT NULL,
  data_nascimento DATE,
  nacionalidade VARCHAR(50)
);

INSERT INTO autores (nome, nacionalidade) 
VALUES ('Machado de Assis', 'Brasil');

SELECT * FROM autores;
```

**Python + MySQL (1.5h)**

```bash
pip install mysql-connector-python
```

**Criar arquivo `conectar_mysql.py`:**
```python
import mysql.connector

class ConexaoDB:
    def __init__(self, host, user, password, database):
        self.conexao = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conexao.cursor()
    
    def executar(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.conexao.commit()
    
    def buscar_todos(self, tabela):
        self.cursor.execute(f"SELECT * FROM {tabela}")
        return self.cursor.fetchall()
    
    def fechar(self):
        self.cursor.close()
        self.conexao.close()

# Uso
db = ConexaoDB('localhost', 'root', 'senha123', 'biblioteca')
autores = db.buscar_todos('autores')
print(autores)
db.fechar()
```

**Exercício:** Criar tabelas para Livros, Empréstimos e consultar dados

---

### **DIA 5-6: Melhorias em POO + Integração Python-MySQL**

#### 🎯 Objetivos:
- Aplicar correções do dia 1 em seus projetos
- Criar classe de acesso a dados com POO
- Type hints e docstrings

#### 📚 Conteúdo:

**Refatorar ContaBancaria com Type Hints + MySQL (2h)**

```python
from typing import Optional
from decimal import Decimal
import mysql.connector

class ContaBancaria:
    """
    Gerencia uma conta bancária com persistência em banco de dados.
    
    Attributes:
        id (int): Identificador único da conta
        titular (str): Nome do titular da conta
        saldo (Decimal): Saldo atual da conta
    """
    
    def __init__(self, titular: str, saldo_inicial: Decimal = Decimal('0.00')) -> None:
        """
        Inicializa uma nova conta bancária.
        
        Args:
            titular: Nome do titular
            saldo_inicial: Saldo inicial (padrão: 0)
            
        Raises:
            ValueError: Se titular vazio ou saldo negativo
        """
        if not titular or len(titular) == 0:
            raise ValueError("Titular não pode estar vazio")
        if saldo_inicial < 0:
            raise ValueError("Saldo inicial não pode ser negativo")
        
        self.titular = titular
        self._saldo = saldo_inicial
    
    @property
    def saldo(self) -> Decimal:
        """Retorna o saldo atual da conta."""
        return self._saldo
    
    def depositar(self, valor: Decimal) -> bool:
        """
        Realiza depósito na conta.
        
        Args:
            valor: Valor a depositar
            
        Returns:
            bool: True se bem-sucedido, False caso contrário
        """
        if valor <= 0:
            raise ValueError("Valor deve ser positivo")
        
        self._saldo += valor
        return True
    
    def sacar(self, valor: Decimal) -> bool:
        """
        Realiza saque na conta.
        
        Args:
            valor: Valor a sacar
            
        Returns:
            bool: True se bem-sucedido
            
        Raises:
            ValueError: Se saldo insuficiente
        """
        if valor <= 0:
            raise ValueError("Valor deve ser positivo")
        if valor > self._saldo:
            raise ValueError("Saldo insuficiente")
        
        self._saldo -= valor
        return True
    
    def __str__(self) -> str:
        return f"Conta de {self.titular}: R${self._saldo:.2f}"


# Classe DAO (Data Access Object) - POO + Banco
class ContaBancariaDAO:
    """Acesso a dados de contas bancárias."""
    
    def __init__(self, conexao: mysql.connector.MySQLConnection) -> None:
        self.conexao = conexao
        self.cursor = self.conexao.cursor()
    
    def criar_tabela(self) -> None:
        """Cria a tabela contas se não existir."""
        query = """
        CREATE TABLE IF NOT EXISTS contas (
            id INT PRIMARY KEY AUTO_INCREMENT,
            titular VARCHAR(100) NOT NULL,
            saldo DECIMAL(10, 2) NOT NULL,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.cursor.execute(query)
        self.conexao.commit()
    
    def salvar(self, conta: ContaBancaria) -> int:
        """Salva uma conta no banco e retorna o ID."""
        query = "INSERT INTO contas (titular, saldo) VALUES (%s, %s)"
        self.cursor.execute(query, (conta.titular, conta.saldo))
        self.conexao.commit()
        return self.cursor.lastrowid
    
    def buscar_por_id(self, conta_id: int) -> Optional[ContaBancaria]:
        """Busca uma conta pelo ID."""
        query = "SELECT titular, saldo FROM contas WHERE id = %s"
        self.cursor.execute(query, (conta_id,))
        resultado = self.cursor.fetchone()
        
        if resultado:
            return ContaBancaria(resultado[0], Decimal(str(resultado[1])))
        return None
    
    def atualizar_saldo(self, conta_id: int, conta: ContaBancaria) -> None:
        """Atualiza o saldo de uma conta."""
        query = "UPDATE contas SET saldo = %s WHERE id = %s"
        self.cursor.execute(query, (conta.saldo, conta_id))
        self.conexao.commit()
```

**Exercício:** Criar testes unitários para a classe

```python
# tests/test_conta_bancaria.py
import unittest
from decimal import Decimal
from seu_modulo import ContaBancaria

class TestContaBancaria(unittest.TestCase):
    
    def setUp(self) -> None:
        self.conta = ContaBancaria("João", Decimal('1000.00'))
    
    def test_deposito_valido(self) -> None:
        self.conta.depositar(Decimal('500.00'))
        self.assertEqual(self.conta.saldo, Decimal('1500.00'))
    
    def test_deposito_negativo_levanta_erro(self) -> None:
        with self.assertRaises(ValueError):
            self.conta.depositar(Decimal('-100.00'))
    
    def test_saque_valido(self) -> None:
        self.conta.sacar(Decimal('300.00'))
        self.assertEqual(self.conta.saldo, Decimal('700.00'))
    
    def test_saque_insuficiente_levanta_erro(self) -> None:
        with self.assertRaises(ValueError):
            self.conta.sacar(Decimal('5000.00'))
    
    def test_titular_vazio_levanta_erro(self) -> None:
        with self.assertRaises(ValueError):
            ContaBancaria("", Decimal('100.00'))

if __name__ == '__main__':
    unittest.main()
```

**Executar testes:**
```bash
python -m pytest tests/ -v
# ou
python -m unittest discover
```

---

### **DIA 7: Projeto Integrado - Sistema de Biblioteca**

#### 🎯 Objetivos:
- Integrar Python + POO + MySQL + Docker
- Criar aplicação pronta para produção

#### 📚 Conteúdo:

**Estrutura do Projeto:**
```
SistemaBiblioteca/
├── docker-compose.yml
├── requirements.txt
├── main.py
├── src/
│   ├── models/
│   │   ├── livro.py
│   │   ├── autor.py
│   │   └── emprestimo.py
│   ├── dao/
│   │   ├── livro_dao.py
│   │   ├── autor_dao.py
│   │   └── emprestimo_dao.py
│   ├── database.py
│   └── utils.py
├── tests/
│   ├── test_livro.py
│   ├── test_emprestimo.py
│   └── conftest.py
└── README.md
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root123
      MYSQL_DATABASE: biblioteca
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      timeout: 5s
      retries: 10

  app:
    build: .
    depends_on:
      mysql:
        condition: service_healthy
    environment:
      DB_HOST: mysql
      DB_USER: root
      DB_PASSWORD: root123
      DB_NAME: biblioteca
    volumes:
      - .:/app

volumes:
  mysql_data:
```

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

**requirements.txt:**
```
mysql-connector-python==8.2.0
python-dotenv==1.0.0
pytest==7.4.0
```

**src/models/livro.py:**
```python
from typing import Optional
from datetime import datetime

class Livro:
    """Representa um livro na biblioteca."""
    
    def __init__(
        self,
        titulo: str,
        autor_id: int,
        isbn: str,
        ano_publicacao: int,
        disponivel: bool = True
    ) -> None:
        """
        Inicializa um novo livro.
        
        Args:
            titulo: Título do livro
            autor_id: ID do autor
            isbn: ISBN único
            ano_publicacao: Ano de publicação
            disponivel: Se está disponível para empréstimo
        """
        if not titulo or len(titulo) < 3:
            raise ValueError("Título deve ter pelo menos 3 caracteres")
        if len(isbn) != 13:
            raise ValueError("ISBN deve ter 13 dígitos")
        if ano_publicacao > datetime.now().year:
            raise ValueError("Ano de publicação não pode ser no futuro")
        
        self.titulo = titulo
        self.autor_id = autor_id
        self.isbn = isbn
        self.ano_publicacao = ano_publicacao
        self.disponivel = disponivel
    
    def __str__(self) -> str:
        status = "Disponível" if self.disponivel else "Emprestado"
        return f"{self.titulo} ({self.ano_publicacao}) - {status}"
    
    def __repr__(self) -> str:
        return f"Livro('{self.titulo}', {self.autor_id}, '{self.isbn}')"
```

**src/dao/livro_dao.py:**
```python
from typing import List, Optional
import mysql.connector
from src.models.livro import Livro

class LivroDAO:
    """Data Access Object para Livro."""
    
    def __init__(self, conexao: mysql.connector.MySQLConnection) -> None:
        self.conexao = conexao
        self.cursor = self.conexao.cursor()
    
    def criar_tabela(self) -> None:
        """Cria a tabela livros."""
        query = """
        CREATE TABLE IF NOT EXISTS livros (
            id INT PRIMARY KEY AUTO_INCREMENT,
            titulo VARCHAR(255) NOT NULL,
            autor_id INT NOT NULL,
            isbn VARCHAR(13) UNIQUE NOT NULL,
            ano_publicacao INT NOT NULL,
            disponivel BOOLEAN DEFAULT TRUE,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (autor_id) REFERENCES autores(id) ON DELETE CASCADE
        )
        """
        self.cursor.execute(query)
        self.conexao.commit()
    
    def inserir(self, livro: Livro) -> int:
        """Insere um livro e retorna o ID."""
        query = """
        INSERT INTO livros (titulo, autor_id, isbn, ano_publicacao, disponivel)
        VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (
            livro.titulo,
            livro.autor_id,
            livro.isbn,
            livro.ano_publicacao,
            livro.disponivel
        ))
        self.conexao.commit()
        return self.cursor.lastrowid
    
    def buscar_por_id(self, livro_id: int) -> Optional[Livro]:
        """Busca um livro pelo ID."""
        query = """
        SELECT titulo, autor_id, isbn, ano_publicacao, disponivel 
        FROM livros WHERE id = %s
        """
        self.cursor.execute(query, (livro_id,))
        resultado = self.cursor.fetchone()
        
        if resultado:
            return Livro(*resultado)
        return None
    
    def listar_disponiveis(self) -> List[Livro]:
        """Lista todos os livros disponíveis."""
        query = """
        SELECT titulo, autor_id, isbn, ano_publicacao, disponivel 
        FROM livros WHERE disponivel = TRUE
        """
        self.cursor.execute(query)
        return [Livro(*row) for row in self.cursor.fetchall()]
    
    def atualizar_disponibilidade(self, livro_id: int, disponivel: bool) -> None:
        """Atualiza a disponibilidade de um livro."""
        query = "UPDATE livros SET disponivel = %s WHERE id = %s"
        self.cursor.execute(query, (disponivel, livro_id))
        self.conexao.commit()
```

**main.py:**
```python
import mysql.connector
from src.database import ConexaoDB
from src.dao.livro_dao import LivroDAO
from src.models.livro import Livro

def main():
    # Conectar ao banco
    db = ConexaoDB()
    livro_dao = LivroDAO(db.conexao)
    
    # Criar tabelas
    livro_dao.criar_tabela()
    
    # Inserir livro de exemplo
    novo_livro = Livro(
        titulo="Dom Casmurro",
        autor_id=1,
        isbn="9788535911769",
        ano_publicacao=1899
    )
    livro_id = livro_dao.inserir(novo_livro)
    print(f"✅ Livro inserido com ID: {livro_id}")
    
    # Buscar livros disponíveis
    livros = livro_dao.listar_disponiveis()
    print(f"\n📚 Livros disponíveis:")
    for livro in livros:
        print(f"  - {livro}")
    
    db.fechar()

if __name__ == "__main__":
    main()
```

**Executar com Docker:**
```bash
docker-compose up -d
docker-compose logs -f app
docker-compose down
```

---

## 📍 **SEMANA 2: Avançado + Otimização**

### **DIA 8-9: Docker Avançado + Compose**

#### 🎯 Objetivos:
- Docker networks
- Volume management
- Orquestração com Docker Compose
- Best practices

#### 📚 Conteúdo:

**Docker Networks (1h)**

```bash
# Criar rede personalizada
docker network create minha-rede

# Conectar container à rede
docker run --name mysql-dev --network minha-rede \
  -e MYSQL_ROOT_PASSWORD=senha \
  -d mysql:8.0

# Conectar container Python à mesma rede
docker run --name python-app --network minha-rede \
  -it python:3.11 bash

# Dentro do container Python:
# Pode fazer ping para: mysql-dev (nome do container)
```

**Docker Compose Avançado (1.5h)**

```yaml
# docker-compose.yml completo
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    container_name: mysql_biblioteca
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_PASSWORD:-root123}
      MYSQL_DATABASE: ${DB_NAME:-biblioteca}
    ports:
      - "${DB_PORT:-3306}:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      timeout: 5s
      retries: 10
      interval: 10s
    restart: unless-stopped

  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: app_biblioteca
    depends_on:
      mysql:
        condition: service_healthy
    environment:
      DB_HOST: mysql
      DB_USER: root
      DB_PASSWORD: ${DB_PASSWORD:-root123}
      DB_NAME: ${DB_NAME:-biblioteca}
      PYTHONUNBUFFERED: 1
    volumes:
      - .:/app
      - /app/__pycache__
    networks:
      - app-network
    restart: unless-stopped
    command: python main.py

networks:
  app-network:
    driver: bridge

volumes:
  mysql_data:
```

**.env.example:**
```
DB_HOST=mysql
DB_USER=root
DB_PASSWORD=seu_password_aqui
DB_NAME=biblioteca
DB_PORT=3306
```

**init.sql - Inicializar dados:**
```sql
USE biblioteca;

CREATE TABLE IF NOT EXISTS autores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    data_nascimento DATE,
    nacionalidade VARCHAR(50)
);

INSERT INTO autores (nome, nacionalidade) VALUES
('Machado de Assis', 'Brasil'),
('Clarice Lispector', 'Brasil'),
('Paulo Coelho', 'Brasil');
```

**Comandos úteis:**
```bash
# Build e start
docker-compose up --build

# Ver logs em tempo real
docker-compose logs -f app

# Executar comando em container
docker-compose exec app python -c "print('teste')"

# Parar tudo
docker-compose down

# Remover volumes também
docker-compose down -v

# Reconstruir imagem
docker-compose up --build --no-deps app
```

---

### **DIA 10-11: MySQL Avançado**

#### 🎯 Objetivos:
- Queries complexas (JOINs, GROUP BY, Subqueries)
- Índices e otimização
- Transações
- Triggers

#### 📚 Conteúdo:

**Schema Completo da Biblioteca:**

```sql
-- Autores
CREATE TABLE autores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL UNIQUE,
    data_nascimento DATE,
    nacionalidade VARCHAR(50),
    biografia TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Livros
CREATE TABLE livros (
    id INT PRIMARY KEY AUTO_INCREMENT,
    titulo VARCHAR(255) NOT NULL,
    autor_id INT NOT NULL,
    isbn VARCHAR(13) UNIQUE,
    ano_publicacao INT,
    disponivel BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (autor_id) REFERENCES autores(id) ON DELETE CASCADE,
    INDEX idx_disponivel (disponivel),
    INDEX idx_isbn (isbn)
);

-- Usuários/Membros
CREATE TABLE membros (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    telefone VARCHAR(11),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT TRUE
);

-- Empréstimos
CREATE TABLE emprestimos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    livro_id INT NOT NULL,
    membro_id INT NOT NULL,
    data_emprestimo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_devolucao_prevista DATE NOT NULL,
    data_devolucao_real DATE,
    multa DECIMAL(10, 2) DEFAULT 0,
    FOREIGN KEY (livro_id) REFERENCES livros(id),
    FOREIGN KEY (membro_id) REFERENCES membros(id),
    INDEX idx_membro (membro_id),
    INDEX idx_livro (livro_id)
);

-- Avaliações
CREATE TABLE avaliacoes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    livro_id INT NOT NULL,
    membro_id INT NOT NULL,
    nota INT CHECK (nota >= 1 AND nota <= 5),
    comentario TEXT,
    data_avaliacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (livro_id) REFERENCES livros(id),
    FOREIGN KEY (membro_id) REFERENCES membros(id),
    UNIQUE KEY unique_avaliacao (livro_id, membro_id)
);
```

**Queries Complexas:**

```sql
-- 1. Livros mais emprestados
SELECT 
    l.titulo,
    a.nome as autor,
    COUNT(e.id) as vezes_emprestado
FROM livros l
JOIN autores a ON l.autor_id = a.id
LEFT JOIN emprestimos e ON l.id = e.livro_id
GROUP BY l.id, l.titulo, a.nome
ORDER BY vezes_emprestado DESC
LIMIT 10;

-- 2. Membros com empréstimos atrasados
SELECT 
    m.nome,
    m.email,
    l.titulo,
    e.data_devolucao_prevista,
    DATEDIFF(CURDATE(), e.data_devolucao_prevista) as dias_atrasado,
    DATEDIFF(CURDATE(), e.data_devolucao_prevista) * 2.00 as multa_calculada
FROM emprestimos e
JOIN membros m ON e.membro_id = m.id
JOIN livros l ON e.livro_id = l.id
WHERE e.data_devolucao_real IS NULL
    AND e.data_devolucao_prevista < CURDATE();

-- 3. Autor com maior avaliação média
SELECT 
    a.nome,
    AVG(av.nota) as nota_media,
    COUNT(DISTINCT av.id) as total_avaliacoes
FROM autores a
JOIN livros l ON a.id = l.autor_id
LEFT JOIN avaliacoes av ON l.id = av.livro_id
GROUP BY a.id, a.nome
HAVING COUNT(DISTINCT av.id) > 0
ORDER BY nota_media DESC;

-- 4. Livros com Subquery
SELECT titulo FROM livros
WHERE id IN (
    SELECT livro_id 
    FROM emprestimos 
    WHERE YEAR(data_emprestimo) = 2024
    GROUP BY livro_id 
    HAVING COUNT(*) > 5
);
```

**Python com Queries Avançadas:**

```python
from typing import List, Dict, Any

class RelatorioDAO:
    """DAO para relatórios complexos."""
    
    def __init__(self, conexao):
        self.conexao = conexao
        self.cursor = self.conexao.cursor(dictionary=True)
    
    def livros_mais_emprestados(self, limite: int = 10) -> List[Dict[str, Any]]:
        """Retorna os livros mais emprestados."""
        query = """
        SELECT 
            l.titulo,
            a.nome as autor,
            COUNT(e.id) as vezes_emprestado
        FROM livros l
        JOIN autores a ON l.autor_id = a.id
        LEFT JOIN emprestimos e ON l.id = e.livro_id
        GROUP BY l.id
        ORDER BY vezes_emprestado DESC
        LIMIT %s
        """
        self.cursor.execute(query, (limite,))
        return self.cursor.fetchall()
    
    def emprestimos_atrasados(self) -> List[Dict[str, Any]]:
        """Retorna empréstimos que estão atrasados."""
        query = """
        SELECT 
            m.nome,
            m.email,
            l.titulo,
            e.data_devolucao_prevista,
            DATEDIFF(CURDATE(), e.data_devolucao_prevista) as dias_atrasado
        FROM emprestimos e
        JOIN membros m ON e.membro_id = m.id
        JOIN livros l ON e.livro_id = l.id
        WHERE e.data_devolucao_real IS NULL
            AND e.data_devolucao_prevista < CURDATE()
        ORDER BY dias_atrasado DESC
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def desempenho_autores(self) -> List[Dict[str, Any]]:
        """Retorna desempenho de cada autor."""
        query = """
        SELECT 
            a.nome,
            COUNT(DISTINCT l.id) as total_livros,
            AVG(av.nota) as nota_media,
            COUNT(DISTINCT e.id) as total_emprestimos
        FROM autores a
        LEFT JOIN livros l ON a.id = l.autor_id
        LEFT JOIN avaliacoes av ON l.id = av.livro_id
        LEFT JOIN emprestimos e ON l.id = e.livro_id
        GROUP BY a.id, a.nome
        ORDER BY total_emprestimos DESC
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
```

**Transações em Python:**

```python
class EmprestimoDAO:
    """DAO para empréstimos com transações."""
    
    def emprestar_livro(self, livro_id: int, membro_id: int, 
                       dias_emprestimo: int = 14) -> bool:
        """
        Realiza empréstimo com transação atômica.
        
        Operações:
        1. Verifica disponibilidade do livro
        2. Marca livro como indisponível
        3. Insere registro de empréstimo
        """
        try:
            self.cursor.execute("START TRANSACTION")
            
            # 1. Verificar disponibilidade
            self.cursor.execute(
                "SELECT disponivel FROM livros WHERE id = %s FOR UPDATE",
                (livro_id,)
            )
            resultado = self.cursor.fetchone()
            if not resultado or not resultado[0]:
                self.cursor.execute("ROLLBACK")
                raise ValueError("Livro não disponível")
            
            # 2. Marcar como indisponível
            self.cursor.execute(
                "UPDATE livros SET disponivel = FALSE WHERE id = %s",
                (livro_id,)
            )
            
            # 3. Inserir empréstimo
            from datetime import datetime, timedelta
            data_devolucao = (datetime.now() + timedelta(days=dias_emprestimo)).date()
            
            self.cursor.execute("""
                INSERT INTO emprestimos 
                (livro_id, membro_id, data_devolucao_prevista)
                VALUES (%s, %s, %s)
            """, (livro_id, membro_id, data_devolucao))
            
            self.conexao.commit()
            return True
            
        except Exception as e:
            self.conexao.rollback()
            raise e
```

---

### **DIA 12-13: Projeto Avançado + Testes**

#### 🎯 Objetivos:
- Implementar todas as funcionalidades
- Testes unitários e integração
- Logging e tratamento de erros
- Deploy local com Docker

#### 📚 Conteúdo:

**Estrutura Final:**
```
SistemaBiblioteca/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
├── main.py
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── logger.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── livro.py
│   │   ├── autor.py
│   │   ├── membro.py
│   │   ├── emprestimo.py
│   │   └── avaliacao.py
│   ├── dao/
│   │   ├── __init__.py
│   │   ├── base_dao.py
│   │   ├── livro_dao.py
│   │   ├── autor_dao.py
│   │   ├── membro_dao.py
│   │   ├── emprestimo_dao.py
│   │   └── relatorio_dao.py
│   └── services/
│       ├── __init__.py
│       └── emprestimo_service.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_models.py
│   ├── test_dao.py
│   ├── test_services.py
│   └── test_integration.py
└── README.md
```

**src/config.py:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configurações da aplicação."""
    
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'root123')
    DB_NAME = os.getenv('DB_NAME', 'biblioteca')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

config = Config()
```

**src/logger.py:**
```python
import logging
from src.config import config

def setup_logger(name: str) -> logging.Logger:
    """Configura logger para um módulo."""
    
    logger = logging.getLogger(name)
    logger.setLevel(config.LOG_LEVEL)
    
    # Handler para console
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger
```

**tests/conftest.py:**
```python
import pytest
import mysql.connector
from src.database import ConexaoDB
from src.config import config

@pytest.fixture
def conexao():
    """Fixture para conexão de teste."""
    db = ConexaoDB()
    yield db
    db.fechar()

@pytest.fixture
def limpar_banco(conexao):
    """Limpa as tabelas antes de cada teste."""
    cursor = conexao.cursor()
    cursor.execute("SET FOREIGN_KEY_CHECKS=0")
    cursor.execute("TRUNCATE TABLE avaliacoes")
    cursor.execute("TRUNCATE TABLE emprestimos")
    cursor.execute("TRUNCATE TABLE membros")
    cursor.execute("TRUNCATE TABLE livros")
    cursor.execute("TRUNCATE TABLE autores")
    cursor.execute("SET FOREIGN_KEY_CHECKS=1")
    conexao.conexao.commit()
    yield
    cursor.close()
```

**tests/test_models.py:**
```python
import pytest
from datetime import datetime
from src.models.livro import Livro
from src.models.autor import Autor
from src.models.membro import Membro

class TestLivro:
    
    def test_criar_livro_valido(self):
        livro = Livro(
            titulo="Dom Casmurro",
            autor_id=1,
            isbn="9788535911769",
            ano_publicacao=1899
        )
        assert livro.titulo == "Dom Casmurro"
        assert livro.disponivel == True
    
    def test_titulo_muito_curto_levanta_erro(self):
        with pytest.raises(ValueError):
            Livro("Dom", 1, "9788535911769", 1899)
    
    def test_isbn_invalido_levanta_erro(self):
        with pytest.raises(ValueError):
            Livro("Dom Casmurro", 1, "123", 1899)
    
    def test_ano_futuro_levanta_erro(self):
        with pytest.raises(ValueError):
            Livro("Livro Futuro", 1, "9788535911769", 2099)

class TestMembro:
    
    def test_criar_membro_valido(self):
        membro = Membro(
            nome="João Silva",
            email="joao@email.com"
        )
        assert membro.nome == "João Silva"
        assert membro.ativo == True
    
    def test_email_invalido_levanta_erro(self):
        with pytest.raises(ValueError):
            Membro("João", "email_invalido")
```

**tests/test_integration.py:**
```python
import pytest
from src.dao.livro_dao import LivroDAO
from src.dao.membro_dao import MembroDAO
from src.dao.emprestimo_dao import EmprestimoDAO
from src.models.livro import Livro
from src.models.membro import Membro

class TestIntegration:
    
    def test_fluxo_completo_emprestimo(self, conexao, limpar_banco):
        """Testa fluxo completo de empréstimo."""
        
        # Setup
        livro_dao = LivroDAO(conexao.conexao)
        membro_dao = MembroDAO(conexao.conexao)
        emprestimo_dao = EmprestimoDAO(conexao.conexao)
        
        # Criar tabelas
        livro_dao.criar_tabela()
        membro_dao.criar_tabela()
        emprestimo_dao.criar_tabela()
        
        # Inserir dados
        livro = Livro("Dom Casmurro", 1, "9788535911769", 1899)
        livro_id = livro_dao.inserir(livro)
        
        membro = Membro("João Silva", "joao@email.com")
        membro_id = membro_dao.inserir(membro)
        
        # Emprestar
        emprestimo_id = emprestimo_dao.emprestar_livro(livro_id, membro_id)
        assert emprestimo_id is not None
        
        # Verificar livro está indisponível
        livro_recuperado = livro_dao.buscar_por_id(livro_id)
        assert livro_recuperado.disponivel == False
```

**main.py - Completo:**
```python
import sys
from src.database import ConexaoDB
from src.dao.livro_dao import LivroDAO
from src.dao.autor_dao import AutorDAO
from src.dao.membro_dao import MembroDAO
from src.dao.emprestimo_dao import EmprestimoDAO
from src.dao.relatorio_dao import RelatorioDAO
from src.logger import setup_logger

logger = setup_logger(__name__)

def inicializar_banco(db: ConexaoDB):
    """Inicializa o banco de dados."""
    logger.info("Inicializando banco de dados...")
    
    autor_dao = AutorDAO(db.conexao)
    livro_dao = LivroDAO(db.conexao)
    membro_dao = MembroDAO(db.conexao)
    emprestimo_dao = EmprestimoDAO(db.conexao)
    
    autor_dao.criar_tabela()
    livro_dao.criar_tabela()
    membro_dao.criar_tabela()
    emprestimo_dao.criar_tabela()
    
    logger.info("✅ Banco inicializado com sucesso")

def menu_principal():
    """Exibe menu principal."""
    print("\n" + "="*40)
    print("📚 SISTEMA DE BIBLIOTECA")
    print("="*40)
    print("1. Cadastrar Autor")
    print("2. Cadastrar Livro")
    print("3. Cadastrar Membro")
    print("4. Emprestar Livro")
    print("5. Devolver Livro")
    print("6. Relatórios")
    print("0. Sair")
    print("="*40)
    return input("Escolha uma opção: ").strip()

def main():
    """Função principal."""
    try:
        db = ConexaoDB()
        inicializar_banco(db)
        
        while True:
            opcao = menu_principal()
            
            if opcao == "0":
                logger.info("Encerrando aplicação...")
                break
            elif opcao == "1":
                print("Função em desenvolvimento...")
            elif opcao == "6":
                relatorio_dao = RelatorioDAO(db.conexao)
                livros = relatorio_dao.livros_mais_emprestados()
                print("\n📊 Livros Mais Emprestados:")
                for livro in livros:
                    print(f"  - {livro['titulo']}: {livro['vezes_emprestado']} empréstimos")
            else:
                print("❌ Opção inválida")
        
        db.fechar()
        
    except Exception as e:
        logger.error(f"Erro: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

**Executar testes:**
```bash
# Com Docker
docker-compose exec app pytest tests/ -v --cov=src

# Localmente
pytest tests/ -v --cov=src --cov-report=html
```

---

### **DIA 14: Revisão + Próximos Passos**

#### 🎯 Objetivos:
- Consolidar aprendizado
- Criar portfólio
- Planejar continuação

#### 📚 Conteúdo:

**Checklist de Aprendizado:**

- [ ] **Docker**
  - [ ] Instalação e configuração
  - [ ] Criar imagens (Dockerfile)
  - [ ] Gerenciar containers
  - [ ] Docker Compose (single e multi-container)
  - [ ] Networks e volumes
  - [ ] Health checks

- [ ] **MySQL**
  - [ ] Criar databases e tabelas
  - [ ] CRUD básico
  - [ ] Relacionamentos (Foreign Keys)
  - [ ] Índices e otimização
  - [ ] Queries complexas (JOINs, GROUP BY, Subqueries)
  - [ ] Transações

- [ ] **Python**
  - [ ] Type hints
  - [ ] Docstrings
  - [ ] Tratamento de erros
  - [ ] Logging

- [ ] **POO**
  - [ ] Encapsulamento
  - [ ] Herança
  - [ ] Polimorfismo
  - [ ] Abstração
  - [ ] Design Patterns (DAO, MVC, Factory)

**Repositório Final:**
```bash
# Criar novo repositório
cd ~/projetos
git clone https://github.com/GuilDiniz/SistemaBiblioteca.git
cd SistemaBiblioteca

# Estrutura pronta para usar
docker-compose up -d
docker-compose exec app pytest tests/ -v
```

**README.md Exemplo:**
```markdown
# 📚 Sistema de Biblioteca

Aplicação full-stack para gerenciamento de biblioteca com Python, MySQL e Docker.

## 🚀 Quick Start

### Pré-requisitos
- Docker Desktop instalado

### Instalação
```bash
# Clone o repositório
git clone https://github.com/GuilDiniz/SistemaBiblioteca.git
cd SistemaBiblioteca

# Configure variáveis de ambiente
cp .env.example .env

# Inicie a aplicação
docker-compose up -d

# Execute testes
docker-compose exec app pytest tests/ -v
```

### Estrutura
- `src/models/` - Classes de domínio
- `src/dao/` - Acesso a dados
- `src/services/` - Lógica de negócio
- `tests/` - Testes automatizados

### Arquitetura
```
┌─────────────────────────────────┐
│     Aplicação Python (OOP)      │
├─────────────────────────────────┤
│    DAOs (Camada de Dados)       │
├─────────────────────────────────┤
│  MySQL (8.0) - Docker Container │
└─────────────────────────────────┘
```

### Contribuindo
1. Faça um fork
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Crie um Pull Request

## 📚 Recursos
- [Docker Docs](https://docs.docker.com/)
- [MySQL Reference](https://dev.mysql.com/doc/)
- [Python OOP](https://docs.python.org/3/tutorial/classes.html)
```

**Próximos Passos Sugeridos:**

1. **REST API com Flask/FastAPI**
   - Transformar o sistema em API REST
   - Adicionar autenticação (JWT)
   - Swagger/OpenAPI

2. **Frontend (HTML/CSS/JS ou React)**
   - Interface web para o sistema
   - Consumir API

3. **CI/CD**
   - GitHub Actions
   - Testes automáticos
   - Deploy automático

4. **Banco de Dados Avançado**
   - Migrations com Alembic
   - ORM com SQLAlchemy
   - Backup e restore

5. **Produção**
   - Deploy em cloud (AWS, GCP, Heroku)
   - Monitoramento e logs
   - Escalabilidade

---

## 📊 **Resumo da Semana**

| Dia | Tecnologia | Tópico | Projeto |
|-----|-----------|--------|---------|
| 1-2 | Docker | Basics + Containers | Primeiro container |
| 3-4 | MySQL | CRUD + Python | Conexão DB |
| 5-6 | Python + POO | Type Hints + OOP | Refatoração |
| 7 | Integração | Projeto Biblioteca (Básico) | Sistema Simples |
| 8-9 | Docker | Compose + Networks | Multi-container |
| 10-11 | MySQL | Queries Avançadas | Relatórios |
| 12-13 | Full Stack | Testes + Logging | Projeto Avançado |
| 14 | Review | Consolidação | Portfólio |

---

## 🎓 **Dicas de Sucesso**

✅ **Estude 2-3h por dia** - Consistência > Intensidade

✅ **Faça todos os exercícios** - Prática leva à proficiência

✅ **Teste seu código frequentemente** - Use Docker para reproducibilidade

✅ **Commit no GitHub** - Documente seu progresso

✅ **Repita conceitos difíceis** - Não pule para o próximo se não entendeu

✅ **Crie projetos próprios** - Aplique o conhecimento

---

## 🔗 **Recursos Importantes**

### Docker
- [Docker Official Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Best Practices](https://docs.docker.com/develop/dev-best-practices/)

### MySQL
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [MySQL Tutorial](https://www.w3schools.com/mysql/)
- [Query Optimization](https://dev.mysql.com/doc/refman/8.0/en/optimization.html)

### Python
- [Python Official Docs](https://docs.python.org/3/)
- [Type Hints PEP 484](https://www.python.org/dev/peps/pep-0484/)
- [Clean Code Python](https://github.com/zedr/clean-code-python)

### POO
- [Design Patterns in Python](https://refactoring.guru/design-patterns/python)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)

---

**Boa sorte com seus estudos! 🚀**
```

Agora vou criar um repositório inicial para você começar:
