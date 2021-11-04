#**************************************
# Build By:
# https://itheo.tech 2021
# MIT License
# Dockerfile to run the ddns.py script
#**************************************

FROM python:3.8-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./ddns.py" ]