# stac-fastapi-taurus
Taurus and Locust load balancing for stac-fastapi

![Alt text](readme_files/taurus-pgstac.png?raw=true "stac-fastapi-pgstac")


## Run stac-fastapi pgstac 
```$ docker-compose build```   
```$ docker-compose up```

## Ingest test data
```$ make ingest```

## Install
```$ pip install .```

## Run Locust Load Balancing Ouside of Taurus Wrapper
```$ stac-taurus --locust```  
- go to ```http://localhost:8089``` and start with desired settings
- for testing locally from docker-compose in this repo, set Host to: ```http://localhost:8083```

## Inside of Taurus Wrapper
```$ stac-taurus --taurus```

## Debugging Locust tasks using a single simulated user
```$ python config_files/locustfile.py```

## References  
  
- https://betterprogramming.pub/introduction-to-locust-an-open-source-load-testing-tool-in-python-2b2e89ea1ff
