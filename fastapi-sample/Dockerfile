FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

# Copy & Change directory
COPY . /app
WORKDIR /app

# pip execution
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt
