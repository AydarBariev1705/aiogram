FROM python:3.10

ENV PYTHONUNBUFFERED=1



COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY admin.py admin.py
COPY bot.py bot.py
COPY config.py config.py
COPY database.py database.py
COPY handlers.py handlers.py
COPY keyboards.py keyboards.py
COPY models.py models.py
COPY payment_handler.py payment_handler.py
COPY states.py states.py
COPY utils.py  utils.py
COPY .env .env
CMD ["python","bot.py","run"]