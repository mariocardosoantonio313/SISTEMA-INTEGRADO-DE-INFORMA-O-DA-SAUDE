# SIIS-UÍGE

Sistema Integrado de Informação da Saúde da Província do Uíge.

## Visão geral

Este projecto implementa a base de uma arquitetura cliente-servidor para gestão da saúde provincial, com:

- cliente desktop em Python usando Tkinter e ttk;
- API em FastAPI para autenticação, dashboard e integração de dados;
- base de dados central PostgreSQL, com SQLAlchemy e Pydantic;
- comunicação por HTTP/HTTPS entre clientes e servidor;
- estrutura modular para expansão em futuros módulos funcionais.

## Estrutura do projecto

```text
SIIS-UIGE/
├── client/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── api_client.py
│   └── views/
│       ├── __init__.py
│       ├── dashboard.py
│       └── login.py
├── database/
│   └── init.sql
├── server/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   └── main.py
├── tests/
│   └── test_auth.py
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── .venv/
```

## Requisitos

- Python 3.12+
- PostgreSQL 15+
- Tkinter (incluído na instalação do Python em Windows)

## Preparação do ambiente

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Configuração da aplicação

1. Copie o ficheiro `.env.example` para `.env`.
2. Ajuste as variáveis de ambiente.
3. Crie a base de dados PostgreSQL localmente.

## Iniciar o servidor

```bash
.venv\Scripts\python -m uvicorn server.main:app --host 0.0.0.0 --port 8000 --reload
```

## Iniciar o cliente desktop

```bash
cd C:\Users\MARIO\SIIS-UIGE
.\.venv312\Scripts\python.exe -m client.main.
```
## Credenciais de teste

Utilize as seguintes credenciais para testar a autenticação na fase inicial do projecto:

- Nome de utilizador: `admin`
- Palavra-passe: `Admin@2026`

> Estas credenciais são apenas para demonstração e devem ser substituídas por valores seguros e reais quando o sistema for implantado.

## Nota

Este projecto entrega uma base funcional, profissional e modular para o SIIS-UÍGE, com autenticação, dashboard e integração do cliente ao servidor em rede local. O desenvolvimento continua por módulos específicos conforme a evolução do sistema.
