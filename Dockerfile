FROM python:3.5.1

# Install pip
RUN apt-get update && apt-get install -y python3-pip

# Install dependencies using pip
RUN pip install flask-restful flask flask-login flask-mail flask-cors flask-sqlalchemy passlib validate_email flask-httpauth
