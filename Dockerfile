FROM python:3.8

WORKDIR /home

COPY    requirements.txt ./requirements.txt
RUN     pip install -r requirements.txt
COPY    . .

EXPOSE  8085
CMD     ["python", "app.py"]