import os


class DBConfig:
    # dbUser = "postgres"
    # dbPass = "admin"
    # host = "db"
    # port = "5432"
    # dbName = "postgres"

    dbUser = os.environ.get('dbUser')
    dbPass = os.environ.get('dbPass')
    dbHost = os.environ.get('dbHost')
    dbPort = os.environ.get('dbPort')
    dbName = os.environ.get('dbName')


class JWTConfig:
    SECRET_KEY = "my_secret_key"
