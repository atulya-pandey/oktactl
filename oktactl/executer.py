import click
import logging
from requests.exceptions import ConnectionError
import traceback


def executer(func):
    def execute(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except ConnectionError:
            click.secho(
                "Invalid credentials provided. \nUse `oktactl configure` command to configure credentials", fg='red')
        except Exception:
            click.secho("Exception occured:\n {}".format(traceback.format_exc()), fg='red')
    
    return execute