FROM python:3.9-slim

RUN     ["mkdir", "-p", "/usr/src/webapp"]

WORKDIR /usr/src/webapp

COPY    ["requirements.txt","."]

RUN     ["pip", "install", "-r", "requirements.txt"]

COPY    [".","."]

CMD     [ "python3", "app.py" ]