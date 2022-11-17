FROM python:3.8

WORKDIR /nelson

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y ffmpeg

RUN apt-get install -y wkhtmltopdf

COPY src/ .

CMD [ "python", "-u", "nelson.py"]