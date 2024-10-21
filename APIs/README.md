# FastAPI Project Setup Guide

This guide provides instructions for setting up and running the FastAPI project for document streaming.

Data Schema and OpenAPI docs is available in `openapi.yaml` file.

## Table of Contents
1. [Running FastAPI Locally](#running-fastapi-locally)
2. [Exporting Test Collection for API Testing](#exporting-test-collection-for-api-testing)
3. [Building and Running Docker Image](#building-and-running-docker-image)

## Running FastAPI Locally

### Prerequisites
Make sure to install the following Python packages:

```bash
pip install kafka-python  # Required for Kafka producer communication
pip install uvicorn[standard]  # To host the server
```

### Starting the Server
1. Navigate to the `app` folder
2. Run the following command:

```bash
uvicorn main:app --reload
```

This will start the FastAPI server with hot-reloading enabled.

## Exporting Test Collection for API Testing

### Prerequisites
- Ensure you've completed the [Running FastAPI Locally](#running-fastapi-locally) section
- Install the following Python package:

```bash
pip install fastapi2postman
```

### Generating Postman Collection
Run the following command in the same directory as your `main.py`:

```bash
fastapi2postman --app main.app --output doc_stream_postman.json
```

This will generate a Postman collection file named `doc_stream_postman.json` for API testing.

## Building and Running Docker Image

### Building the Docker Image
Run the following command to build the Docker image:

```bash
docker build -t api-ingest .
```

This will create a Docker image named `api-ingest`.

### Running the Docker Container
You have two options for running the Docker container:

#### Option 1: Run with Custom Network
To run the container on the same network as other services:

```bash
docker run --rm --network document-streaming_default --name my-api-ingest -p port_num:port_num api-ingest
```

#### Option 2: Run with Local Port Mapping
To run the container with just a port mapping to your local machine:

```bash
docker run --rm --name my-api-ingest -p port_num:port_num api-ingest
```

This option allows you to access the API from your local machine at `http://localhost:80`.

## Additional Information

- The `fastapi2postman` tool is useful for generating Postman collections, which can be imported into Postman for API testing.
- When running the Docker container, the `--rm` flag ensures that the container is removed after it stops, which is useful for development and testing.
- The `-p port_num:port_num` flag maps the container's port port_num to your host's port port_num. Adjust this if you need to use a different port on your host machine.
 - run `client/code/get_api_docs.py` to obtain the documentation in yaml format.

For more information on FastAPI, Docker, or Kafka, refer to their respective official documentation:
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Kafka Documentation](https://kafka.apache.org/documentation/)