import click
import requests
import json
from .utils import get_api_info
from .executer import executer


@executer
def list_users_dec():
    base_url, headers = get_api_info()
    url = "{}/users?limit=200".format(base_url)
    user_list = []

    response = requests.get(url, headers=headers)

    for user in json.loads(response.text):
        user_list.append("{} {}".format(
            user['profile']['firstName'], user['profile']['lastName']))
    click.secho("User List: {}".format(user_list), fg='green')


@executer
def create_user_dec(password, number, login, email, last_name, first_name):
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


@executer
def create_groups_and_assign_to_app_dec():
    base_url, headers = get_api_info()
    group_url = "{}/groups".format(base_url)
    group_name_list = []
    group_desc_list = []
    successfully_created_groups = []
    failed_groups = []

    while True:
        group_name_list.append(click.prompt("Group name"))
        group_desc_list.append(click.prompt("Group Description"))
        if not click.confirm('Do you want create one more group?'):
            break

    app_id = click.prompt("App id")

    for group_name, group_desc in zip(group_name_list, group_desc_list):
        group_data = json.dumps({
            "profile": {
                "name": group_name,
                "description": group_desc
            }
        })
        group_response = requests.post(
            group_url, data=group_data, headers=headers)
        if group_response.status_code == 200:
            group_details = json.loads(group_response.text)
            group_id = group_details['id']
            successfully_created_groups.append(group_name)

            app_url = "{}/apps/{}/groups/{}".format(base_url, app_id, group_id)
            app_response = requests.put(app_url, headers=headers)
            if app_response.status_code == 200:
                click.secho(
                    "Group '{}' created successfully and has been assigned to app '{}'".format(group_name, app_id), fg='green')
            else:
                click.secho(
                    "Group '{}' created successfully and but couldn't be assigned to the app '{}'. ErrorSummary: {}".format(group_name, app_id, json.loads(app_response._content)['errorSummary']), fg='red') 
        else:
            failed_groups.append(group_name)
    if successfully_created_groups:
        click.secho("\nList of groups created successfully: {}".format(
            successfully_created_groups), fg='green')
    if failed_groups:
        click.secho("\nFailed to create these groups: {}.\nErrorSummary: {}".format(
            failed_groups, json.loads(group_response._content)['errorCauses'][0]['errorSummary']), fg='red')
