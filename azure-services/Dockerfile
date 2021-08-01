FROM python:3.8-slim-buster

# Copy & Change directory
COPY . /app/
WORKDIR /app

# library update
RUN apt-get update

# pip execution
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install azure-cosmos
RUN pip install pandas

# Set Environment Variables
ARG ACCOUNT_URI
ENV ACCOUNT_URI=${ACCOUNT_URI}
ARG ACCOUNT_KEY
ENV ACCOUNT_KEY=${ACCOUNT_KEY}

CMD ["python", "cosmos-db.py"]
