# Simple docker run fastapi backend

Open terminal in correct directory. Current working directory is in this folder. 

```
ls
```
Result 
```
Dockerfile  fastapi_app.py  README.md  requirements.txt
```

### 1. Build docker image 
```
docker build -t my-fastapi-app-with-postgresql .
```
Add `sudo` if above command do not work (ubuntu, linux only)
```
sudo docker build -t my-fastapi-app-with-postgresql .
```

Explain:

- build: tell docker engine to build image from Dockerfile. Build context is . (the dot, current directory)
- `-t` name of image 

### 2. Run docker image 


We need to run the postgresql database first. 


```
docker run -d --name my-postgres-db \
-p 10000:5432 \
-v ./src:/app \
-e POSTGRES_PASSWORD=mysecretpassword \
postgres:17.2
```

- `-d`: run in background, no lock terminal, turn off terminal does not kill container
- `--name`: name of container
- `-p`: port forwarding
    -  10000 is port expose outside to host machine. 
    -  5432 is port in container 
- `-v`: volume mapping
- `-e`: environment variable
    - `POSTGRES_PASSWORD=mysecretpassword` is password for postgresql
- `postgres`: name of image

```
docker run -p 8111:8000 \
--name my-fastapi-container \
--link my-postgres-db:db \
-d \
-e DATABASE_URL=postgresql://postgres:mysecretpassword@db:5432/postgres \
my-fastapi-app-with-postgresql
```


Explain: 
- `run`: tell docker to start a container use `my-fastapi-app` image 
- `-p`: port forwarding, map <host-pc-port>:<container-port>, so the example above, it map localhost:8000 to 0.0.0.0:8000 inside container
- `-d`: run in background, no lock terminal, turn off terminal does not kill container 
- `--name`: name of container
- `--link`: link container to another container, in this case, link to `my-postgres-db` container
- `-e`: environment variable, use environment variable `DATABASE_URL` to connect to postgresql database


### 3. Test if it work 

```
curl localhost:8111
```


Insert some data into postgresql database.

```
curl -X 'POST' \
  'http://127.0.0.1:8111/notes/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "note_number_1",
  "content": "This is note number 1"
}'


curl -X 'POST' \
  'http://127.0.0.1:8111/notes/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "note_number_2",
  "content": "This is note number 2"
}'




```


Get notes 
```
curl -X 'GET' \
  'http://127.0.0.1:8111/notes/note_number_1' \
  -H 'accept: application/json'


curl -X 'GET' \
  'http://127.0.0.1:8111/notes/note_number_2' \
  -H 'accept: application/json'


```

### 4. Clean up - delete container

Looking for container, stop and delete container. Add `sudo` if command does not work.

```
docker container ls -a 
```

- `-a` show all container, without `-a` only show active container

Result 
```
CONTAINER ID   IMAGE                         COMMAND                  CREATED         STATUS                      PORTS                                       NAMES
233d5a02783b   my-fastapi-app                "uvicorn fastapi_app…"   4 minutes ago   Up 4 minutes                0.0.0.0:8000->8000/tcp, :::8000->8000/tcp   charming_cartwright
```

Container name is set at random, or you can set container name by using argument `--name` at `docker run`

Stop container then delete container. Use container id or container name 

```
docker container stop 233d5a02783b
docker container rm 233d5a02783b
```

```
docker container stop charming_cartwright
docker container rm charming_cartwright
```

### 5. Clean up - delete image

List image. add `sudo` if it not work. 

```
docker image ls
```
Result
```
REPOSITORY                        TAG       IMAGE ID       CREATED          SIZE
my-fastapi-app                    latest    3848805893a3   7 minutes ago    135MB
```

Delete image with image name (REPOSITORY) or image id
```
docker image rm my-fastapi-app
```
OR
```
docker image rm 3848805893a3
```