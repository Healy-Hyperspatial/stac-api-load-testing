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
@click.command()
@click.version_option(version="0.1.4")
def main(ingest, locust, taurus, backend):
    """
    Entry point for the stac-api-load-balancing CLI tool.

    This function serves as the command-line interface for a tool designed to facilitate
    testing and interacting with a STAC (SpatioTemporal Asset Catalog) API across different
    backends. It allows the user to ingest sample data, run Locust tests directly, or
    execute Taurus performance tests based on the specified backend.

    Args:
        ingest (bool): If True, triggers the ingestion of sample data into the specified backend.
        locust (bool): If True, runs Locust load testing directly outside of the Taurus wrapper.
        taurus (bool): If True, executes Taurus performance testing for the specified backend.
        backend (str): Specifies the backend to be used. Can be one of 'pgstac', 'es', or 'mongo'.
                       This choice determines the host URL and the configuration file used for testing.

    The function sets the LOCUST_HOST environment variable based on the selected backend to ensure
    that load tests target the correct host. It then performs the action specified by the command-line
    arguments: ingesting data with the data_loader module for sample data setup, or running load tests
    using Locust or Taurus with configurations tailored to the selected backend.
    """
    port, config_file = backend_to_config_map.get(
        backend, ("8083", "taurus_locust_pgstac.yml")
    )
    host = f"http://localhost:{port}"

    os.environ["LOCUST_HOST"] = host

    if ingest:
        data_loader.load_items(stac_api_base_url=host)
    elif locust:
        # Run Locust directly with the determined host
        os.system(f"locust --locustfile config_files/locustfile.py --host {host}")
    elif taurus:
        # Run Taurus with the configuration file corresponding to the chosen backend
        config_file_path = f"config_files/{config_file}"
        os.system(f"bzt {config_file_path}")


if __name__ == "__main__":
    main()
