FROM python:3.7-slim

# Set working directory
WORKDIR /usr/app

# App specific requirements
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Add app
COPY ./pictures ./pictures

# Add entrypoint.sh
RUN chmod +x ./pictures/entrypoint.sh

# User
USER nobody

# Run
CMD ["./pictures/entrypoint.sh"]
