FROM python:3.8-slim-buster

WORKDIR /app

# library update
RUN apt-get update

# pip execution
COPY ../requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip3 install azure-cosmos
RUN pip3 install pandas

COPY . .
CMD ["python3", "cosmos-db.py"]
