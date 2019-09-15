import click
import os
from .okta import list_users_dec, create_groups_and_assign_to_app_dec, create_user_dec, delete_groups_dec


@click.group()
@click.version_option()
def okta():
    pass

# ============================== Configure Credentials ==============================


@okta.command('configure')
def configure():
    domain_name = click.prompt('Domain name')
    api_token = click.prompt('API token')

    okta_dir = os.path.expanduser("~/.okta_cli")
    if not os.path.exists(okta_dir):
        os.mkdir(okta_dir)
    f = open("{}/credentials".format(okta_dir), "w")
    f.write("domain_name: {0}\napi_token: {1}".format(domain_name, api_token))
    f.close()


# ==================================== User API Commands ====================================

@okta.command('list-users')
def list_users():
    list_users_dec()


@click.option('--password', prompt='User\'s password', help='User\'s password', hide_input=True)
@click.option('--number', prompt='User\'s phone number', help='User\'s phone number')
@click.option('--login', prompt='User\'s login id', help='User\'s login id')
@click.option('--email', prompt='User\'s email id', help='User\'s email id')
@click.option('--last-name', prompt='User\'s last name', help='User\'s last name')
@click.option('--first-name', prompt='User\'s first name', help='User\'s first name')
@okta.command('create-user')
def create_user(password, number, login, email, last_name, first_name):
    create_user_dec(password, number, login, email, last_name, first_name)


# ==================================== Group API Commands ====================================

@okta.command('create-groups-and-assign-to-app')
def create_groups_and_assign_to_app():
    create_groups_and_assign_to_app_dec()


@okta.command('delete-groups')
def delete_groups():
    delete_groups_dec()
