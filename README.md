# Backend Challenge

Este repositório contém um desafio de backend com instruções para rodar o projeto utilizando Docker ou, opcionalmente, um ambiente Python local para depuração.

---

## ✅ Pré-requisitos

Certifique-se de ter instalado:

- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- (Opcional) [Python 3.11+](https://www.python.org/) e `venv` para execução local

---

## 🚀 Instruções de execução com Docker (recomendado)

```bash
# Clone o repositório
git clone https://github.com/LucasMalagoli/backend-challenge
cd backend-challenge

# Copie o arquivo de ambiente
cp .env.example .env

# Construa e suba os containers
docker-compose up --build
````

---

## 🐛 Execução local (opcional para depuração)

```bash
# Crie e ative o ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Inicialize o banco de dados
docker-compose up db --build

# Inicialize o servidor
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

> **Importante**: se for rodar localmente sem Docker, altere o valor da variável `DATABASE_URL` no arquivo `.env`:
>
> Substitua o nome do host `db` por `localhost`.

---

## Documentação

Após inicialização local ou via docker, estará disponível em http://localhost:8000/docs

---

## ⚠️ Observações

* O valor da variável `DATABASE_URL` em `.env.example` está preenchido apenas para fins ilustrativos do desafio.
* Certifique-se de configurar corretamente o ambiente antes de executar os comandos.

---

## 🛠️ Tecnologias

* Python 3
* Docker
* Docker Compose
* PostgreSQL (via Docker)
