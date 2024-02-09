FROM python:3.11.7-slim-bullseye

WORKDIR /srv

COPY srv/requirements.txt .

RUN pip install -r requirements.txt

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]