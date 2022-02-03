FROM python:3.8

WORKDIR /nelson

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y ffmpeg

COPY src/ .

CMD [ "python", "./nelson.py"]