import click
import os
import sys

sys.path
sys.executable

@click.option("-l", "--locust", is_flag=True, help="Run Locust outside of the Taurus wrapper.")
@click.option("-t", "--taurus", is_flag=True, help="Run the Taurus wrapper.")
@click.command()
# @click.argument('file')
@click.version_option(version="0.1.4")
def main(locust, taurus):
    if locust:
        os.system('locust --locustfile config_files/locustfile.py')
    if taurus:
        os.system('bzt config_files/taurus_locust.yml')