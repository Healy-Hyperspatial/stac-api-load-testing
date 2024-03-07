import click
import os
import sys
from data_loader import data_loader

# Map backend names to their respective port numbers and Taurus YAML configuration files
backend_to_config_map = {
    'pgstac': ('8083', 'taurus_locust_pgstac.yml'),
    'es': ('8084', 'taurus_locust_es.yml'),
    'mongo': ('8085', 'taurus_locust_mongo.yml'),
}

@click.option("-i", "--ingest", is_flag=True, help="Ingest sample data for a chosen backend.")
@click.option("-l", "--locust", is_flag=True, help="Run Locust outside of the Taurus wrapper.")
@click.option("-t", "--taurus", is_flag=True, help="Run the Taurus wrapper based on the specified backend.")
@click.option("-b", "--backend", type=click.Choice(['pgstac', 'es', 'mongo'], case_sensitive=False), default='pgstac', help="Specify the backend for Locust or Taurus execution.")
@click.command()
@click.version_option(version="0.1.4")
def main(ingest, locust, taurus, backend):
    port, config_file = backend_to_config_map.get(backend, ('8083', 'taurus_locust_pgstac.yml'))
    host = f"http://localhost:{port}"

    os.environ["LOCUST_HOST"] = host

    if ingest:
        data_loader.load_items(stac_api_base_url=host)
    elif locust:
        # Run Locust directly with the determined host
        os.system(f'locust --locustfile config_files/locustfile.py --host {host}')
    elif taurus:
        # Run Taurus with the configuration file corresponding to the chosen backend
        config_file_path = f'config_files/{config_file}'
        os.system(f'bzt {config_file_path}')

if __name__ == "__main__":
    main()
