FROM python:3.8-slim
WORKDIR /usr/app
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./tg_bot ./tg_bot
COPY ./logging.json ./logging.json
CMD ["python", "tg_bot/bot.py"]