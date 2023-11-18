# Documentação

Documentação e passo a passo do projeto
## Depêndencias a serem instaladas

- [Python ^3.0](https://www.python.org/downloads/)
- [Docker](https://docs.docker.com/engine/install/)
- [Docker-Compose](https://docs.docker.com/compose/install/)

## Iniciando aplicação

- Inicializar os containers executando o comando:

```bash
docker-compose up --build
```

## Acessando container da aplicação

- Para acessar o container da aplicaçao e executar os comandos python executar seguinte comando:

```bash
docker exec -it bym_backend sh
```

- Para acessar o container do banco e executar os comandos sql executar seguinte comando:

```bash
docker exec -it bym_db sh -c "mysql -u root -p'root' bym"
```

## Executando Migrações

- No container `bym_backend` executar os seguintes comandos

```bash
python3 /app/manage.py makemigrations
python3 /app/manage.py migrate
```

## Criando super usuário para django admin

Executar comando para criar novo usuário:

```bash
python3 /app/manage.py createsuperuser
```

## Referências

- https://www.djangoproject.com/
- https://www.django-rest-framework.org/
- https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django
- https://www.rabbitmq.com/documentation.html
- https://www.python.org/doc/

