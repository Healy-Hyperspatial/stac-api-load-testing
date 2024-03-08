"""stac-api-load-balancing cli tool."""
import os
import re
import subprocess

import click
import pkg_resources  # type: ignore
import yaml  # type: ignore

from .data_loader import data_loader


def generate_taurus_config(api_url):
    """Generate a Taurus configuration file with the specified API URL."""
    template_path = pkg_resources.resource_filename(
        __name__, "config_files/taurus_locust.yml"
    )
    print("template path: ", template_path)
    locustfile_path = pkg_resources.resource_filename(
        __name__, "config_files/locustfile.py"
    )

    safe_api_url = re.sub(r"[^a-zA-Z0-9]+", "_", api_url)
    output_path = f"taurus_config_{safe_api_url}.yml"

    try:
        with open(template_path, "r") as file:
            config = yaml.safe_load(file)

        # Setting the script path directly to where `locustfile.py` is expected to be within the package
        config["scenarios"]["default"]["script"] = locustfile_path
        config["scenarios"]["default"]["default-address"] = api_url

        with open(output_path, "w") as file:
            yaml.safe_dump(config, file)

        return output_path
    except Exception as e:
        print(f"Error creating Taurus configuration file: {e}")
        return None


@click.option(
    "-i", "--ingest", is_flag=True, help="Ingest sample data into the STAC API."
)
@click.option(
    "-l", "--locust", is_flag=True, help="Run Locust load tests against the STAC API."
)
@click.option(
    "-t",
    "--taurus",
    is_flag=True,
    help="Run the Taurus wrapper for performance testing against the STAC API.",
)
@click.option(
    "-a",
    "--api-address",
    default="http://localhost:8080",
    help="Specify the STAC API URL to test against.",
)
@click.command()
@click.version_option(version="0.1.0")
def main(ingest, locust, taurus, api_address):
    """
    Entry point for the stac-api-load-balancing CLI tool.

    This tool facilitates data ingestion, Locust load testing, and Taurus performance testing
    against a specified STAC API endpoint.

    Args:
        ingest (bool): If true, ingests sample data into the specified STAC API.
        locust (bool): If true, conducts Locust load testing against the STAC API.
        taurus (bool): If true, performs Taurus performance testing against the STAC API.
        api_address (str): The URL of the STAC API for testing.
    """
    os.environ["LOCUST_HOST"] = api_address

    if ingest:
        data_loader.load_items(stac_api_base_url=api_address)
    elif locust:
        subprocess.run(
            [
                "locust",
                "--locustfile",
                pkg_resources.resource_filename(__name__, "config_files/locustfile.py"),
                "--host",
                api_address,
            ],
            check=True,
        )
    elif taurus:
        config_file_path = generate_taurus_config(api_address)
        if config_file_path:
            try:
                subprocess.run(["bzt", config_file_path], check=True)
            finally:
                if os.path.exists(config_file_path):
                    os.remove(config_file_path)  # Cleanup the temporary config file


if __name__ == "__main__":
    main()
