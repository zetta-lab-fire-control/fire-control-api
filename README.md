
# 🔥 Fire Control API

Uma API construída com **FastAPI**, utilizando **uv** para gerenciamento de pacotes Python. Todo o ecossistema é conteinerizado com Docker, incluindo proxy reverso com Nginx, banco de dados PostgreSQL, cache com Redis e storage com MinIO.

---

## 📂 Estrutura do Projeto

A arquitetura do repositório foi pensada para separar claramente a infraestrutura do código-fonte e da documentação:

* **`deploy/`**: Contém toda a infraestrutura como código.
    * **`compose/dev.yml`**: Arquivo do Docker Compose para o ambiente local.
    * **`containers/`**: Dockerfiles e configurações específicas de cada serviço (FastAPI, Nginx, PostgreSQL, Redis, MinIO).
    * **`variables/`**: Arquivos de variáveis de ambiente (`.env`).
* **`docs/`**: Documentação detalhada de arquitetura, requisitos e casos de uso do projeto.
* **`source/`**: O coração da aplicação.
    * **`api/`**: Código-fonte da API (FastAPI), incluindo rotas (`routes/`) e o arquivo principal (`app.py`).
    * **`tests/`**: Testes automatizados da aplicação.
* **`pyproject.toml` e `uv.lock`**: Arquivos de dependências Python gerenciados pelo `uv`.
* **`Makefile`**: Atalhos e comandos úteis para facilitar o desenvolvimento.

---

## 🛠️ Dependências e Tecnologias

Para executar este projeto localmente, você precisará apenas das seguintes ferramentas instaladas na sua máquina:

1.  **[Docker](https://docs.docker.com/get-docker/)** e **Docker Compose** (Essencial para rodar a infraestrutura).
2.  **[Make](https://www.gnu.org/software/make/)** (Para utilizar os atalhos do `Makefile`).

### Stack Tecnológica (Serviços)
* **Backend:** Python 3.13 / FastAPI / Uvicorn
* **Gerenciador de Pacotes:** uv
* **Banco de Dados:** PostgreSQL 18
* **Cache:** Redis
* **Object Storage:** MinIO
* **Proxy Reverso/Gateway:** Nginx (configurado para HTTPS local)

---

## 🚀 Como Executar o Projeto Localmente

O ambiente de desenvolvimento foi automatizado via `Makefile` e Docker Compose para subir com o mínimo de esforço.

### Subindo a infraestrutura

No terminal, na raiz do projeto, execute o comando abaixo para construir as imagens e subir todos os contêineres:

```bash
make dev-start
```

Nota: Na primeira vez, o Docker irá baixar as imagens base (Postgres, Redis, MinIO, etc.) e o `uv` compilará as dependências do Python dentro do contêiner `api`.

### Acessando a API

O Nginx está configurado como um gateway para a aplicação, interceptando o tráfego e garantindo conexão segura (HTTPS).

  * **URL Base da API:** Acesse através de **`https://localhost:8000`**

    *(Como o certificado SSL de desenvolvimento é autoassinado, o seu navegador exibirá um aviso de segurança. Basta clicar em "Avançado" e prosseguir para o localhost).*

### 3 Documentação Interativa (Swagger UI)

Com os contêineres rodando, o FastAPI gera automaticamente a documentação interativa da API. Você pode visualizar todas as rotas, testar requisições e verificar os schemas de dados acessando:

👉 **[https://localhost:8000/docs](https://www.google.com/search?q=https://localhost:8000/docs)**

-----

## 🛑 Parando a aplicação

Para parar e remover os contêineres (sem perder os dados dos volumes de banco de dados e storage), utilize o comando do Make correspondente (ex: `make dev-stop` ou `docker compose -f deploy/compose/dev.yml down`).
