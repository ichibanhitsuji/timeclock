# Timeclock Project

## About

The project consists of building a simple application serving a GraphQL API for employees to clock in and out, and also for them to check the number of hours worked today, on the current week, and on the current month.

It is using the follwing stack: 
- Django
- Graphene
- Graphene-Django
- Django-GraphQL-JWT
- Freezegun ( for testing purposes)

Please check that the package are installed

```shell
pip install django
pip install graphene
pip install graphene-django
pip install django-graphql-jwt
pip install freezegun
```

# Running the project

Database is not included in the project. You can create a database manually or use the following command to create a database:
```shell
python manage.py makemigrations
python manage.py migrate
```

To run the project:
```shell
python manage.py runserver
```

I let the default admin interface to be used at: [http://localhost:8000/admin/](http://localhost:8000/admin/)
The graphql playground to test the project is at: [http://localhost:8000/graphql/](http://localhost:8000/graphql/)

# Running the tests
```shell
python manage.py test
```
