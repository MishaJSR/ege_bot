FROM python:3.10-alpine
WORKDIR /usr/src/app/bot
COPY requirements.txt /usr/src/app/bot
RUN pip install -r /usr/src/app/botrequirements.txt
COPY . /usr/src/app/bot