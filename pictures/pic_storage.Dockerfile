# docker build --file=pictures/pic_storage.Dockerfile --tag=salamantos/fancy_weather:pic_storage-1.0.0 .
FROM python:3.7-slim

# Set working directory
WORKDIR /usr/app

# Add pictures
COPY ./pictures/pic_storage ./pic_storage
