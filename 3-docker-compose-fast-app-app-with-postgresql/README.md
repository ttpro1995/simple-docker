# 3-Docker Compose Fast App with PostgreSQL
=============================================

This project demonstrates a simple FastAPI application with a PostgreSQL database using Docker Compose.

## Table of Contents
-----------------

* [Prerequisites](#prerequisites)
* [Project Structure](#project-structure)
* [Setup](#setup)
* [Run the Application](#run-the-application)
* [API Endpoints](#api-endpoints)

## Prerequisites
---------------

* Docker installed on your machine
* Docker Compose installed on your machine

## Project Structure
-------------------

The project consists of the following directories and files:

* `fastapi-app`: The FastAPI application code
	+ `src`: The source code for the application
		- `fastapi_app.py`: The main application file
		- `requirements.txt`: The dependencies required by the application
	+ `Dockerfile`: The Dockerfile for building the application image
* `init_db.sql`: The SQL script for initializing the PostgreSQL database
* `docker-compose.yml`: The Docker Compose file for defining the services

## Setup
--------

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Run `docker-compose up -d --build` to start the application.


## Test the application 

Write some curl 

```
curl -X 'POST' \
  'http://127.0.0.1:8222/notes/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "note_number_3",
  "content": "This is note number 3"
}'
```