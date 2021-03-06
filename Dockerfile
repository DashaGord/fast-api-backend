# Dockerfile

# pull the official docker image
FROM python:3

# set work directory
WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .
#
# CMD ["python", "app/main.py"]
