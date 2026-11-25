# 🦷 Sorriso Fácil

## Sobre o projeto

O Sorriso Fácil é um sistema que desenvolvi com a ideia de ajudar na organização de um consultório odontológico. Nele, é possível cadastrar pacientes, organizar consultas e consultar as informações de maneira simples.

Esse projeto foi feito como parte de uma atividade do curso Técnico em Desenvolvimento de Sistemas. Durante o desenvolvimento, pude colocar em prática alguns conhecimentos que aprendi nas aulas.

## O que o sistema faz?

- Mostra uma página inicial com informações do sistema.
- Permite cadastrar pacientes.
- Mostra a lista de pacientes cadastrados.
- Permite pesquisar pacientes pelo nome.
- Permite editar e excluir pacientes.
- Permite cadastrar consultas.
- Mostra as consultas cadastradas.
- Permite editar e excluir consultas.
- Relaciona as consultas com os pacientes.
- Possui uma API que mostra os pacientes em formato JSON.

 ## Como funciona a pesquisa

A pesquisa de pacientes foi feita utilizando Python. O sistema percorre a lista de pacientes e compara os nomes com o que foi digitado na busca.

Utilizei uma estrutura de repetição while e uma condição if para verificar os resultados. Também usei lower() para que a pesquisa funcione mesmo quando são utilizadas letras maiúsculas ou minúsculas.

## Tecnologias que utilizei

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- Jinja2

## Banco de dados

Para guardar as informações, utilizei o SQLite.

O banco de dados possui duas tabelas principais:

**Pacientes:** guarda informações como nome, telefone e e-mail.

**Consultas:** guarda informações como data, horário, procedimento e status da consulta.

As duas tabelas são relacionadas, pois um mesmo paciente pode ter várias consultas cadastradas.

## Como executar o projeto

Para abrir o sistema no computador, é necessário seguir alguns passos:

**1.** Ter o Python instalado.

**2.** Abrir a pasta do projeto no Visual Studio Code.

**3.** Abrir o terminal e criar o ambiente virtual:

```bash
python -m venv venv
```

**4.** Ativar o ambiente virtual:

```bash
venv\Scripts\activate
```

**5.** Instalar as dependências:

```bash
pip install -r requirements.txt
```

**6.** Iniciar o sistema:

```bash
python app.py
```

**7.** Abrir o navegador e acessar:

http://127.0.0.1:5000/

## API

Também desenvolvi uma rota que permite visualizar os pacientes cadastrados em formato JSON.

O endereço da rota é:

```text
/api/pacientes
```

Para testar no computador:

http://127.0.0.1:5000/api/pacientes

## Acesso ao projeto

O sistema está publicado na internet e pode ser acessado pelo link:

https://sorriso-facil.onrender.com

O código também está disponível no GitHub:

https://github.com/Kauaravi/sorriso-facil

## O que aprendi com esse projeto

Durante a criação do Sorriso Fácil, consegui praticar melhor a programação em Python, a criação de páginas com HTML e CSS e o uso de banco de dados.

Também aprendi um pouco mais sobre como conectar o sistema ao banco de dados, organizar as funções e publicar um projeto na internet.

## Observação

Este projeto foi desenvolvido apenas para fins de estudo e utiliza dados fictícios. Por isso, não deve ser utilizado para guardar informações reais de pacientes.