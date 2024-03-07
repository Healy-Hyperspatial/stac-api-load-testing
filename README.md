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

Options:
  --version                       Show the version and exit.
  -b, --backend [pgstac|es|mongo]
                                  Specify the backend for Locust or Taurus
                                  execution.
  -t, --taurus                    Run the Taurus wrapper based on the
                                  specified backend.
  -l, --locust                    Run Locust outside of the Taurus wrapper.
  -i, --ingest                    Ingest sample data for a chosen backend.
  --help                          Show this message and exit.
```

## Ingest test data (es|pgstac|mongo)
```$ stac-api-load-balancing --ingest --backend es```

## Run Locust Load Balancing Ouside of Taurus Wrapper
```$ stac-api-load-balancing --locust```  
- go to ```http://localhost:8089``` and start with desired settings
- for testing locally from docker-compose in this repo, set Host to: ```http://localhost:8083```

## Inside of Taurus Wrapper
```$ stac-api-load-balancing --taurus```

## Debugging Locust tasks using a single simulated user
```$ python config_files/locustfile.py```
