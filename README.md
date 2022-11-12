## Project: Foodgram - The Grocery Assistant

![Status of workflow runs triggered by the push event](https://github.com/nastyatonkova/foodgram-project-react/actions/workflows/main.yml/badge.svg?event=push)

## Availability
178.154.202.65

## Description
Online service and API for it. On this service, users will be able to publish recipes, subscribe to other users' publications, add favorite recipes to the "Favorites" list, and before going to the store, download a summary list of products needed to prepare one or more selected dishes.

![Main Web-Page View](https://user-images.githubusercontent.com/77447030/201496440-7dd60304-4b82-45f5-a759-d30ed44ccf11.png)

![Recipe View](https://user-images.githubusercontent.com/77447030/201496462-b0bc02c8-6200-40af-91a0-05545c3123ed.png)


***
## Workflow
Runs when you push to the `master` branch, does not run if the commit was only edited file `README.md`

Consists of the following steps:

`tests`: installing dependencies, running flake8 and pytest

`build_and_push_foodgram_backend_to_docker_hub`: build a foodgram_backend image and upload it to your repository on DockerHub

`build_and_push_foodgram_frontend_to_docker_hub`: build a foodgram_frontend image and upload it to your repository on DockerHub

`deploy`: deploying the project on a remote server

`send_message`: sending a notification to telegram Chat when a successful workflow in GitHub Actions is passed

***
### Preparing and launching a project in Docker

***
Clone the repository:

```
git clone https://github.com/nastyatonkova/foodgram-project-react.git
```

***
Create an .env file of environment variables and put the necessary information there:
- Django SECTRET_KEY secret key used for hashing and cryptographic signatures. You can generate your key, for example, at https://djecrety.ir/ or by running the following command in the terminal:
```
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
- information regarding the PostgreSQL DB

- list of allowed hosts as host_1,host_2,host_n (comma separated, no spaces)

- place the configured infra/.env file on the remote server in home/<your_username>/.env

***
Example of filling in infra/.env

```
SECRET_KEY=YOUR_SECRET_KEY_FOR_SETTINGS.PY (your secret key from settings.py)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<<<database password>>>
DB_HOST=db
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1,host_1,host_2,host_N(Use a comma without spaces. Add also the names of the containers created by the docker. For example, containers backend, frontend, db, nginx)
DEBUG=False (on poduction)
```

***
### Installation on a remote server (Ubuntu):
1\. Log in to your remote server:

```
ssh <your_login>@<ip_address>
```

2\. Install Docker on a remote server:

```
sudo apt install docker.io
```

3\. Install docker-compose on a remote server:
 - Check what the latest version is available on the [releases page](https://github.com/docker/compose/releases 'https://github.com/docker/compose/releases').
 - The following command downloads version 2.12.2 and saves the executable file in the `/usr/local/bin/docker-compose`, which will cause the software to be globally available under the name `docker-compose`:

```
sudo curl -L "https://github.com/docker/compose/releases/download/v2.12.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

- Then you must set the correct permissions to make the docker-compose command executable:

```
sudo chmod +x /usr/local/bin/docker-compose
```

- To check if the installation was successful, run the following command:

```
docker-compose --version
```

- The output will look like this:

```
Docker Compose version v2.12.2
```

4\. Copy files `infra/.env`, `infra/docker-compose.yaml` and `infra/nginx.conf` from the project to the remote server in `home/<your_username>/.env`, `home/<your_username>/docker-compose.yaml` и `home/<your_username>/nginx.conf` respectively.

```
scp infra/.env <username>@<host>:/home/<username>/infra/.env
scp infra/docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
scp -r infra/nginx.conf <username>@<host>:/home/<username>/nginx.conf
```

5\. Add environment variables to Secrets on GitHub:

```
DOCKER_USERNAME=<<<<<<username DockerHub>>>
DOCKER_PASSWORD=<<<password DockerHub>>>
REMOTE_USER=<<<username remote server>>>
REMOTE_HOST=<<<IP-address of remote server>>>
TELEGRAM_TO=<<<ID of your telegram account>>>
TELEGRAM_TOKEN=<<<your bot's token>>>
SSH_KEY=<<<SSH private key, can be obtained by running the command on the local machine: cat ~/.ssh/id_rsa>>>
```

***
### After deploy

Go to the remote server and execute in turn the commands to create migrations, create a superuser and collect statics:

```
sudo docker-compose exec backend python manage.py makemigrations
sudo docker-compose exec backend python manage.py migrate
sudo docker-compose exec backend python manage.py createsuperuser
sudo docker-compose exec backend python manage.py collectstatic --no-input
```

***
```
The project will be available at: `http://<IP-address of remote server>/`

Admin at: `http://<IP-address of remote server>/admin/`

General documentation at: `http://<IP-address of remote server>/api/docs/`

If a domain name is registered, you can use it instead of the IP address of the remote server. The same goes for the https protocol.
```

***
You need to log in to the admin as a superuser, created earlier, and add there to the section `Tags` required number of tags for the recipe in the format:

`Name`

`Random color in hex format #FFFFFF`

`Unique slug for the link`

Tags can be different. For example, `Breakfast`, `Lunch`, `Dinner`, `Sweets`. You can assign multiple tags to one recipe, but at least one.

***
In the admin panel, you can add a list of ingredients. When creating a recipe, the user selects ingredients from the list provided by the service. You can import a fairly large pre-prepared list of ~2800 items by running the command:

```
sudo docker-compose exec backend python manage.py import_to_db
```

***
When creating a recipe in the service, enter the name of the ingredient in the corresponding field, and if it is present in the list, it will be displayed. ingredient names are case-sensitive.

***
### Stopping Docker
If the command does not execute and the terminal says there is a lack of rights, insert `sudo` before the command.

To stop the containers without removing them, run the command:

```
sudo docker-compose stop
```

To stop with the removal of containers and internal networks associated with these services:

```
sudo docker-compose down
```

To stop with the removal of containers, internal networks associated with these services, and volumes:

```
sudo docker-compose down -v
```

***
### Starting a Docker project after stopping it

To start a previously stopped project if containers have not been deleted:

```
sudo docker-compose start -d
```

To start a previously stopped project if containers were deleted, but volumes were not:

```
sudo docker-compose up -d
```

