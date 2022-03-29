"""Create a secret.py file in the root directory
   of the project with secret key and DB information.
"""
from django.core.management.utils import get_random_secret_key


def main():
    # Ask for database information
    db_name = input('Database name: ')
    db_user = input('Database username: ')
    db_password = input('Database password: ')
    db_host = input('Database host: ')
    db_port = input('Database port: ')
    sentry_dsn = input('Sentry DSN: ')

    secret_key = get_random_secret_key()
    secret_file = open('secret.py', 'w')
    secret_file.write(f'DJANGO_SECRET_KEY = "{secret_key}"')
    secret_file.write('\n\n')
    secret_file.write(f'NAME_DB = "{db_name}"')
    secret_file.write(f'USERNAME_DB = "{db_user}"')
    secret_file.write(f'PASSWORD_DB = "{db_password}"')
    secret_file.write(f'HOST_DB = "{db_host}"')
    secret_file.write(f'PORT_DB = "{db_port}"')
    secret_file.write(f'SENTRY_DSN = "{sentry_dsn}"')
    secret_file.close()


if __name__ == '__main__':
    main()
