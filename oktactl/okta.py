import click
import requests
import json
import csv
from .utils import get_api_info
from .executer import executer
import random
import time
from tqdm import tqdm
import os


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
    group_name_list = []
    group_desc_list = []

    option = click.prompt(
        "Option 1: Provide inputs manually\nOption 2: Read through CSV file\n",
        type=int
    )

    if option == 1:
        while True:
            group_name_list.append(click.prompt("Group name"))
            group_desc_list.append(click.prompt("Group Description"))
            if not click.confirm('Do you want create one more group?'):
                break

    elif option == 2:
        csv_file_path = click.prompt("Path of CSV file", type=str)
        with open(csv_file_path,'rt') as f:
            data = csv.reader(f)
            for group_name, group_description in data:
                group_name_list.append("{}-{}".format(group_name, random.randint(1,1000001)))
                group_desc_list.append(group_description)
    
    else:
        click.secho("Incorrect option selected", fg='red')
        create_groups_and_assign_to_app_dec()
    
    create_groups_and_assign_to_app_dec_utility(group_name_list, group_desc_list)

def create_groups_and_assign_to_app_dec_utility(group_name_list, group_desc_list):
    base_url, headers = get_api_info()
    group_url = "{}/groups".format(base_url)
    successfully_created_groups = {}
    failed_groups = {}

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
            successfully_created_groups[group_name] = {'id': group_id, 'desc': group_desc}
            app_url = "{}/apps/{}/groups/{}".format(base_url, app_id, group_id)
            app_response = requests.put(app_url, headers=headers)

            if app_response.status_code == 200:
                click.secho(
                    "Group '{}' created successfully and has been assigned to app '{}'".format(group_name, app_id), fg='green')
            else:
                click.secho(
                    "Group '{}' created successfully and but couldn't be assigned to the app '{}'. ErrorSummary: {}".format(group_name, app_id, json.loads(app_response._content)['errorSummary']), fg='red') 
        else:
            failed_groups[group_name] = {'id': None, 'desc': group_desc}
    if successfully_created_groups:
        click.secho("\nList of groups created successfully: {}".format(
            [key for key in successfully_created_groups.keys()]), fg='green')
    if failed_groups:
        click.secho("\nFailed to create these groups: {}.\n".format([key for key in failed_groups.keys()]), fg='red')
    merged_dictionary = successfully_created_groups.copy()
    merged_dictionary.update(failed_groups)

    create_groups_and_assign_to_app_post_action(merged_dictionary)

def create_groups_and_assign_to_app_post_action(group_details):
    current_wd = os.getcwd()
    with open('{}/group-details-log.csv'.format(current_wd), mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerows([group_name, group_details[group_name]['desc'], group_details[group_name]['id'],] for group_name in group_details)
    click.secho("Log file generated: {}/group-details-log.csv".format(current_wd))

@executer
def delete_groups_dec():
    base_url, headers = get_api_info()
    group_url = "{}/groups".format(base_url)
    group_response = requests.get("{}?limits={}".format(group_url, 200), headers=headers)
    group_details = json.loads(group_response.text)
    groups_id_list = [item['id'] for item in group_details]

    successfully_deleted_groups = []
    failed_groups = []

    for group_id in tqdm(groups_id_list):
        group_response = requests.delete("{}/{}".format(group_url, group_id), headers=headers)
        if group_response:
            successfully_deleted_groups.append(group_id)
        else:
            failed_groups.append(group_id)
    
    if successfully_deleted_groups:
        click.secho("\nList of groups deleted successfully: {}".format(
            successfully_deleted_groups), fg='green')
    if failed_groups:
        click.secho("\nFailed to delete these groups: {}.\n".format(failed_groups), fg='red')

    