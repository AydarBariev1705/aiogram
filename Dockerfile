FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /bot
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY bot .
COPY .env .env
CMD ["python","bot.py","run"]