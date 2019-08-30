import click
import logging
from requests.exceptions import ConnectionError


def executer(func):
    def execute(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except ConnectionError:
            click.secho(
                "Invalid credentials provided. \nUse `oktactl configure` command to configure credentials", fg='red')
        except Exception as exc:
            logging.info("Exception occured: ", exc_info=exc)
    
    return execute