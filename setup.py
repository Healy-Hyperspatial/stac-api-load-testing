"""stac-api-load-balancing setup.py
"""
from setuptools import setup

__version__ = "0.1.0"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="stac_api_load_balancing",
    version=__version__,
    description="Load balancing for stac compliant apis",
    url="https://github.com/Healy-Hyperspatial/stac-api-load-balancing",
    include_package_data=True,
    install_requires=[
        "click>=7.1.2",
        "locust",
        "setuptools",
        "Cython",
        "bzt",
    ],
    packages=["stac_api_load_balancing"],
    entry_points={
        'console_scripts': ['stac-api-load-balancing=stac_api_load_balancing.cli:main']
    },
    author="Jonathan Healy",
    author_email="jonathan.d.healy@gmail.com",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    tests_require=["pytest"]
)