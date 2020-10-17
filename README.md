# Todo Application

- Problem statement

Create a to-do application where the following functionalities are present -
1. User can create, delete and edit a to-do.
2. They should also be able to mark a to-do done and vice-versa.
3. They should be able to create a to-do under a bucket. The user has the flexibility to name this bucket according to his/her choice.
a. All the existing buckets the user has created should be given as options, next time the user tries to create a new bucket.

# Technologies used
- [Django](https://www.djangoproject.com/): The web framework for perfectionists with deadlines (Django builds better web apps with less code).
- [DRF](https://www.django-rest-framework.org/): A powerful and flexible toolkit for building Web APIs

# Docker images used
- [frolvlad/alpine-python3](https://hub.docker.com/r/frolvlad/alpine-python3) - for base image

# Prerequisites
- Install Docker
> $ curl -fsSL https://get.docker.com -o get-docker.sh
> $ sudo sh get-docker.sh
- Install Git
> $ sudo apt install git

# Installation
- Clone repo & cd to project directory
> $ git clone https://github.com/anonyxhappie/todo-backend.git; cd todo-backend
- Rename settings.ini.example & update values in settings.ini
> $ mv settings.ini.example settings.ini; vim settings.ini
- Create local directory to mount with container
> $ mkdir -p /tmp/todofiles
- Create docker image
> $ docker build -t todoapp:v1 .
- Run todo api server
> $ docker run -v /tmp/todofiles:/tmp/todofiles -it -p 8000:8000 todoapp:v1

# Check logs
> $ tail -f /tmp/todofiles/todo_project_debug.log

# API Documentation
> https://www.getpostman.com/collections/ffac577242d3c5bf8503
