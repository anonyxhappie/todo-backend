# set the base image 

FROM frolvlad/alpine-python3

# create working directory

RUN mkdir -p /todo/todoproject

# create directory to mount

RUN mkdir -p /tmp/todofiles

# set directoty where CMD will execute 

WORKDIR /todo/todoproject

# add project files to the /todo/todoproject folder

COPY todoproject ./

# add settings.ini file

COPY settings.ini /todo/

# add requirements.txt file

COPY requirements.txt ./

# get pip to download and install requirements:

RUN pip install --no-cache-dir -r requirements.txt

# Create DB Schema 

RUN python3 /todo/todoproject/manage.py migrate

# Expose ports

EXPOSE 8000

# default command to execute      

CMD python3 /todo/todoproject/manage.py runserver --insecure 0.0.0.0:8000