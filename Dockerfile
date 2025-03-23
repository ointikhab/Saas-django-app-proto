# Use the official Python image
FROM python:3.11
# ignore pyc filess
ENV PYTHONDONTWRITEBYTECODE = 1
ENV PYTHONUNBUFFERED = 1

# Set the working directory
WORKDIR /dockerdjangosetup

# Copy project files into the container
COPY requirements.txt /dockerdjangosetup/

RUN pip install -r requirements.txt

COPY . /dockerdjangosetup/