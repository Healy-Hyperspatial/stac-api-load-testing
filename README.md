# stac-api-load-balancing
Taurus and Locust load balancing tools for testing stac-api backends.

![Alt text](readme_files/taurus-pgstac.png?raw=true "stac-fastapi-pgstac")


## Run stac-fastapi pgstac (elasticsearch|pgstac)
```$ docker-compose up pgstac```   
```$ docker-compose up app-pgstac```

## Install
```$ pip install .```  

```
Usage: stac-api-load-balancing [OPTIONS]

  Entry point for the stac-api-load-balancing CLI tool.

  This tool facilitates data ingestion, Locust load testing, and Taurus
  performance testing against a specified STAC API endpoint.

Args:     
  ingest (bool): If true, ingests sample data into the specified STAC API.     
  locust (bool): If true, conducts Locust load testing against the STAC API.     
  taurus (bool): If true, performs Taurus performance testing against the STAC API.     
  api_address (str): The URL of the STAC API for testing.  

Options:
  --version               Show the version and exit.
  -a, --api-address TEXT  Specify the STAC API URL to test against.
  -t, --taurus            Run the Taurus wrapper for performance testing
                          against the STAC API.
  -l, --locust            Run Locust load tests against the STAC API.
  -i, --ingest            Ingest sample data into the STAC API.
  --help                  Show this message and exit.
```

## Ingest test data
```$ stac-api-load-balancing --ingest --api-address http://localhost:8084```

## Run Locust Load Balancing Ouside of Taurus Wrapper
```$ stac-api-load-balancing --locust --api-address http://localhost:8084```  
- go to ```http://localhost:8089``` and start with desired settings

## Inside of Taurus Wrapper
```$ stac-api-load-balancing --taurus --api-address http://localhost:8084```

## Debugging Locust tasks using a single simulated user
```$ python stac_api_load_balancing/config_files/locustfile.py```
