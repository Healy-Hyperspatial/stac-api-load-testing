"""stac-api-load-balancing cli tool."""
import os

import click

from data_loader import data_loader

# Map backend names to their respective port numbers and Taurus YAML configuration files
backend_to_config_map = {
    "pgstac": ("8083", "taurus_locust_pgstac.yml"),
    "es": ("8084", "taurus_locust_es.yml"),
    "mongo": ("8085", "taurus_locust_mongo.yml"),
}


@click.option(
    "-i", "--ingest", is_flag=True, help="Ingest sample data for a chosen backend."
)
@click.option(
    "-l", "--locust", is_flag=True, help="Run Locust outside of the Taurus wrapper."
)
@click.option(
    "-t",
    "--taurus",
    is_flag=True,
    help="Run the Taurus wrapper based on the specified backend.",
)
@click.option(
    "-b",
    "--backend",
    type=click.Choice(["pgstac", "es", "mongo"], case_sensitive=False),
    default="pgstac",
    help="Specify the backend for Locust or Taurus execution.",
)
@click.option(
    "-a",
    "--api-address",
    default=None,
    help="Specify a custom API address for testing, overriding the backend-derived address.",
)
@click.command()
@click.version_option(version="0.1.0")
def main(ingest, locust, taurus, backend, api_address):
    """
    Entry point for the stac-api-load-balancing CLI tool.

    Allows the user to optionally specify a custom API address for testing,
    ingest sample data, run Locust tests directly, or execute Taurus
    performance tests based on the specified backend or custom API address.

    Args:
        ingest (bool): If True, triggers the ingestion of sample data into the specified backend.
        locust (bool): If True, runs Locust load testing directly outside of the Taurus wrapper.
        taurus (bool): If True, executes Taurus performance testing for the specified backend.
        backend (str): Specifies the backend to be used. Options are 'pgstac', 'es', or 'mongo'.
                       Determines the host URL and configuration file for testing if no custom API address is provided.
        api_address (str, optional): Custom API address for testing, overrides backend-derived address.
                                     Example format: 'http://custom-api:port'.
    """
    host = (
        api_address
        if api_address
        else f"http://localhost:{backend_to_config_map[backend][0]}"
    )

    os.environ["LOCUST_HOST"] = host

    if ingest:
        data_loader.load_items(stac_api_base_url=host)
    elif locust:
        # Run Locust directly with the determined or specified host
        os.system(f"locust --locustfile config_files/locustfile.py --host {host}")
    elif taurus:
        # If using a custom API address with Taurus, consider how you'll handle configuration since
        # Taurus configurations are pre-defined for each backend. You might need a more dynamic approach or separate handling.
        config_file_path = f"config_files/{backend_to_config_map[backend][1]}"
        os.system(f"bzt {config_file_path}")


if __name__ == "__main__":
    main()
