FROM python:3.8

WORKDIR /home

COPY    requirements.txt ./requirements.txt
RUN     pip install -r requirements.txt
COPY    . .

EXPOSE  8081
CMD     ["python", "app.py"]