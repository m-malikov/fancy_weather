FROM python:3.8-slim
WORKDIR /usr/app
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./poems ./poems
CMD ["./poems/entrypoint.sh"]

