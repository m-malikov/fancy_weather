FROM python:3.7-slim
#RUN apt-get update && apt-get install -y gcc build-essential curl cron

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

