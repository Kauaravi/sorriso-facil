
# 🦷 Sorriso Fácil

## Sobre o projeto

O Sorriso Fácil é um sistema web desenvolvido para auxiliar na organização de um consultório odontológico. A ideia do projeto é facilitar o gerenciamento de pacientes e consultas, reunindo informações importantes em um único lugar.

O sistema foi desenvolvido como parte de uma atividade prática do curso Técnico em Desenvolvimento de Sistemas, utilizando tecnologias que foram estudadas durante o curso.

## Funcionalidades

- Página inicial com resumo do sistema.
- Cadastro de pacientes.
- Listagem e pesquisa de pacientes.
- Edição e exclusão de pacientes.
- Cadastro de consultas odontológicas.
- Listagem de consultas.
- Edição e exclusão de consultas.
- Pesquisa de pacientes por nome utilizando Python.
- API que disponibiliza os pacientes em formato JSON.

## Tecnologias utilizadas

- Python
- Flask
- SQLite
- HTML5
- CSS3
- JavaScript
- Jinja2

## Banco de dados

O sistema utiliza SQLite para armazenar os dados.

O banco possui duas tabelas principais:

### Pacientes

Armazena os dados dos pacientes cadastrados, como nome, telefone e e-mail.

### Consultas

Armazena as informações dos agendamentos, como data, horário, procedimento e status da consulta.

As tabelas estão relacionadas. Um paciente pode possuir várias consultas cadastradas.

## Como executar o projeto

1. Instale o Python no computador.
2. Abra a pasta do projeto no Visual Studio Code.
3. Abra o terminal.
4. Instale as dependências com o comando:

   pip install -r requirements.txt

5. Execute o sistema:

   python app.py

6. Abra o navegador e acesse:

   http://127.0.0.1:5000/

## API

O projeto possui uma rota que disponibiliza os pacientes em formato JSON.

Endpoint:

/api/pacientes

Para testar localmente:

http://127.0.0.1:5000/api/pacientes

## Objetivo

O objetivo do projeto é aplicar na prática os conhecimentos de desenvolvimento web, programação em Python, banco de dados e organização de sistemas, criando uma aplicação que simula uma necessidade real da área da saúde.

## Observação

Este projeto possui finalidade educacional e utiliza dados fictícios. Não deve ser utilizado para armazenar informações reais de pacientes.
