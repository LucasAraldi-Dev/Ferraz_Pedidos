# Ferraz - Pedidos
![GitHub version](https://img.shields.io/badge/version-0.3.2-blue)


## Descrição

**Ferraz - Pedidos** é um WebApp desenvolvido com FastAPI, MongoDB e autenticação baseada em JWT, que gerencia pedidos de produtos para setores específicos. 

Ele oferece funcionalidades como:
- Criação de novos pedidos
- Edição de pedidos existentes
- Listagem de todos os pedidos
- Controle de acesso por autenticação JWT

## Tecnologias Utilizadas

- **[Python](https://www.python.org/)**: Linguagem de programação principal do projeto.
- **[FastAPI](https://fastapi.tiangolo.com/)**: Framework para desenvolvimento de APIs de uma forma rápida.
- **[JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)**: Utilizado no front-end para fazer a interação com o Front.
- **[MongoDB](https://www.mongodb.com/)**: Banco de dados NoSQL para armazenamento dos pedidos e usuários.
- **[Motor](https://motor.readthedocs.io/)**: Driver assíncrono para integração com MongoDB.
- **[OAuth2 com JWT](https://oauth.net/2/)**: Sistema que utilizamos para autenticação seguro usando JSON Web Tokens.

## Versão

A versão atual do projeto é **0.3.2**.

A próxima atualização **(0.4.0)** está planejada para reformular completamente o design da aplicação, trazendo uma interface mais intuitiva e moderna.

## Funcionalidades

- **Autenticação JWT**: Somente usuários autenticados podem criar, listar e editar pedidos.
- **Registro de Usuários**: Permite o registro de novos usuários no sistema.
- **CRUD de Pedidos**: Funcionalidades de Criação, Leitura, Atualização e Exclusão de pedidos.

## Instalação

### Pré-requisitos

- **Python 3.10+**
- **MongoDB** (local ou em um servidor)

