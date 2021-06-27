FROM python:3.8

WORKDIR /nelson

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ .

CMD [ "python", "./nelson.py"]