# Toggl to Redmine

Essa aplicação é um _fork_ do projeto "Automatic Toggl Import" feito pelo Rodrigo Marques. Seu intuito é oferecer uma versão em linha de comando para o lançamento automatizado de horas do Toggl para o Redmine.

## Arquitetura

Todo o código fonte relacionado ao _import_ de horas foi desacoplado da plataforma na qual o usuário está interagindo.

Exemplificando: o _core_ da aplicação é o `toggl_to_redmine(config)`. Porém, o _entry point_ da aplicação é feito através de uma subclasse de `Platform`.

Dessa forma, é possível reutilizar todo o código com a lógica de negócios através de interfaces de interação distintas facilmente. O `Platform` utilizado pode ser visto no `main.py`.

## TODO

* Fazer uma wiki explicando como instalar e usar
