## How to run local development instance of backend
* Install dependencies through pipenv (make sure to run it in directory with ***Pipfile***)
```
pipenv install
```
* Enter virtual environment (make sure to run it in directory with ***Pipfile***)
```
pipenv shell
```
* Create local instance of postgres database, for example:
```
sudo su - postgres
psql
CREATE DATABASE database_name;
CREATE USER database_owner_user WITH PASSWORD 'databse_user_password';
ALTER ROLE database_owner_user SET client_encoding TO 'utf8';
ALTER ROLE database_owner_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE database_owner_user SET timezone TO 'Europe/Warsaw';
GRANT ALL PRIVILEGES ON DATABASE database_name TO database_owner_user;
```
* Provide environmental variables (e.g in .env file):
```
SECRET_KEY=some_secret_key
DB_NAME=database_name
DB_USER=database_owner_user
DB_PASSWORD=databse_user_password
DB_HOST=localhost
DB_PORT=5432
DEBUG=1
```
* Set environmental variables, for example (with .env file):
```
export $(xargs < .env)
```
* Run migrations
```
python3 manage.py migrate
```
* Run server
```
python3 manage.py runserver
```