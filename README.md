# CNH Importer


## Build

To create the Docker image run:

```
docker build -t cnh-importer .
```

## Running on Docker

To run the docker container run the following command:

Make sure to add the volume binding to access to the logs files.
See .run/Dockerfile.run.xml to see an example.
```
docker run cnh-importer -v $HOME/CNHi:/data
```