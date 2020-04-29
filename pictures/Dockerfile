FROM salamantos/fancy_weather:pic_storage-1.0.0

# Set working directory
WORKDIR /usr/app

# App specific requirements
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Add app
COPY ./pictures .

# Add entrypoint.sh
RUN chmod +x entrypoint.sh

# User
USER nobody

# Run
CMD ["./entrypoint.sh"]

