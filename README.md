# Settlekaro
![hld-diagram-settlekaro](https://github.com/user-attachments/assets/e79b2368-4549-46c0-b106-ce6a99fe1616)

## Description
An application for settling your bills amongst friends. Many a time you have to split and settle expenses. Settlekaro will help you do that.

## How to run the services

- Before running the services in docker, make sure you have installed docker and docker-compose

- Run the command:
```
docker compose up 
```
to bring up the services. This will run a local instance of postgres and migrations will automatically run for you.

## How to run Docker locally with your own hosted postgres
In case you don't want to run the psql in docker and want to run migrations and services on a hosted postgres.

- First create a .env file in the root
``` touch .env ```

- Give the following environment variables in the env file
```
FLASK_APP=app.py
DATABASE_URI=<YOUR_HOSTED_PG_URL>
JWT_SECRET_KEY=<SECRET_JWT_KEY>
```

- After doing all the above steps, run the docker locally
```
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" settlekaro-api sh -c "flask run --host 0.0.0.0"
```
this will run the app on port 5000 and any changes in the repository will be reflected automatically.

#### NOTE - $(pwd) works only in Mac and Linux, for Windows use `cd` command.
