FROM python:3.8-slim
WORKDIR /usr/app
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./core ./core
COPY ./core.config core.config
CMD ["python", "core/app.py", "--config", "core.config"]

