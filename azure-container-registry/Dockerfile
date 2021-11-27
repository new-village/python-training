FROM python:3.8-slim-buster

# Copy & Change directory
COPY . /app/
WORKDIR /app

# library update
RUN apt-get update

# pip execution
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install pandas

ENTRYPOINT ["python", "main.py"]
