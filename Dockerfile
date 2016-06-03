FROM python:3.5.1

# Install pip
RUN apt-get update && apt-get install -y python3-pip

WORKDIR /source-files

# Copy pip requirements to image
COPY requirements.txt /tmp/

# Install dependencies using pip
RUN pip install --requirement /tmp/requirements.txt

# Expose the correct port
EXPOSE 5000


ENTRYPOINT ["python", "api.py"]