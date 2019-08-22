import click
import requests
import os
import logging
import json
from requests.exceptions import ConnectionError
from .utils import get_api_info


@click.group()
@click.version_option()
def okta():
    pass


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


@okta.command('list-users')
def list_users():
    base_url, headers = get_api_info()
    url = "{}/users?limit=200".format(base_url)
    user_list = []
    try:
        response = requests.get(url, headers=headers)
        for user in json.loads(response.text):
            user_list.append("{} {}".format(
                user['profile']['firstName'], user['profile']['lastName']))
        click.secho("User List: {}".format(user_list), fg='green')
    except ConnectionError:
        click.secho(
            "Invalid credentials provided. \nUse `okta configure` command to configure credentials", fg='red')
    except Exception as exc:
        logging.info("Exception occured: ", exc_info=exc)


@click.option('--password', prompt='User\'s password', help='User\'s password', hide_input=True)
@click.option('--number', prompt='User\'s phone number', help='User\'s phone number')
@click.option('--login', prompt='User\'s login id', help='User\'s login id')
@click.option('--email', prompt='User\'s email id', help='User\'s email id')
@click.option('--last-name', prompt='User\'s last name', help='User\'s last name')
@click.option('--first-name', prompt='User\'s first name', help='User\'s first name')
@okta.command('create-user')
def create_user(password, number, login, email, last_name, first_name):
    base_url, headers = get_api_info()
    url = "{}/users?activate=false".format(base_url)
    data = json.dumps(
        {
            "profile": {
                "firstName": first_name,
                "lastName": last_name,
                "email": email,
                "login": login,
                "mobilePhone": number
            },
            "credentials": {
                "password": {
                    "value": password
                }
            }
        }
    )

    try:
        response = requests.post(url, data=data, headers=headers)
        if response.status_code == 200:
            user_details = json.loads(response.text)
            click.secho(
                "User created successfully with user-id: {}".format(user_details['id']), fg='green')
        else:
            error_message = 'Error occured while creating user: \n'
            for message in json.loads(response._content)['errorCauses']:
                error_message = error_message + message['errorSummary'] + '\n'
            click.secho("{}".format(error_message), fg='red')
    except ConnectionError:
        click.secho(
            "Invalid credentials provided. \nUse `okta configure` command to configure credentials", fg='red')
    except Exception as exc:
        logging.exception("Exception occured: ", exc_info=exc)


@okta.command('create-groups')
def create_groups():
    base_url, headers = get_api_info()
    group_url = "{}/groups".format(base_url)
    group_name_list = []
    group_desc_list = []
    successfully_created_groups = []
    failed_groups = []
    
    while True:
        group_name_list.append(click.prompt("Group name"))
        group_desc_list.append(click.prompt("Group Desccription"))
        if not click.confirm('Do you want create more groups?'):
            break
    
    app_id = click.prompt("App id")

    for group_name, group_desc in zip(group_name_list, group_desc_list):
        group_data = json.dumps({
            "profile": {
                "name": group_name,
                "description": group_desc
            }
        })
        try:
            group_response = requests.post(group_url, data=group_data, headers=headers)
            if group_response.status_code == 200:
                group_details = json.loads(group_response.text)
                group_id = group_details['id']
                successfully_created_groups.append(group_name)
                
                app_url = "{}/apps/{}/groups/{}".format(base_url, app_id, group_id)
                app_response = requests.put(app_url, headers=headers)
                if app_response.status_code == 200:
                    click.secho(
                        "Group '{}' created successfully and has been assigned to app {}".format(group_name, app_id), fg='green')
            else:
                failed_groups.append(group_name)
        except ConnectionError:
            click.secho(
                "Invalid credentials provided. \nUse `okta configure` command to configure credentials", fg='red')
    if successfully_created_groups:
        click.secho("List of groups created successfully: {}".format(successfully_created_groups), fg='green')
    if failed_groups:
        click.secho("Failed to create these groups: {}".format(failed_groups), fg='red')

