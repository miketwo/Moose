FROM python:2.7

RUN mkdir /app
WORKDIR /app
COPY apt-requirements.txt /app

RUN apt-get update && apt-get install -y $(grep -vE "^\s*#" apt-requirements.txt  | tr "\n" " ")

COPY requirements.txt /app
RUN pip install pygame
RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["/bin/bash", "./entrypoint.sh"]

CMD ["game"]
