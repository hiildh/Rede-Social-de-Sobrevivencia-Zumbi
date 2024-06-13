# Zombie Survivor Social Network (ZSSN)

## Descrição do Projeto

Este projeto é uma rede social para sobreviventes de um apocalipse zumbi compartilharem recursos e informações entre si.

## Tecnologias Utilizadas

- Django: framework web para desenvolvimento rápido em Python.
- Django REST Framework: uma poderosa e flexível toolkit para construir Web APIs.
- Vue.js: um framework progressivo para construir interfaces de usuário.

## Instalação

### Pré-requisitos

- Python 3.x instalado
- Node.js e npm instalados

### Passos para Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/zombie-survivor-social-network.git
   cd zombie-survivor-social-network
2. Instale as dependências Python:
    ```bash
    pip install -r requirements.txt
3. Instale as dependências Vue.js:
    ```bash
    cd frontend
    npm install
4. Configure o banco de dados e migre as tabelas:
    ```bash
    python manage.py migrate
5. Inicie o servidor Django:
    ```bash
    python manage.py runserver
6. Inicie o servidor de desenvolvimento Vue.js:
    ```bash
    cd frontend
    npm run serve
Acesse a aplicação no navegador em http://localhost:8080.

## Funcionalidades Principais
### Registro de Sobreviventes
**Rota**: ```/register-survivor/```

**Descrição**: Permite o cadastro de novos sobreviventes com nome, idade, gênero, localização e inventário.

### Dashboard do Sobrevivente
**Rota**: ````/survivors/current/````

**Descrição**: Exibe informações detalhadas do sobrevivente logado, incluindo seu inventário e opções para atualizar localização, reportar infecção e trocar itens.
### Relatórios
**Rota**: ``/reports/``

**Descrição**: Exibe estatísticas globais como porcentagem de sobreviventes infectados, média de recursos por sobrevivente e pontos perdidos de inventário por sobreviventes infectados.
### Troca de Itens
**Rota**: ````/inventories/{survivor}/trade/````

**Descrição**: Permite a troca de itens entre dois sobreviventes.
