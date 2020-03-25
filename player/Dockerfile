FROM raspbian/jessie

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install libraspberrypi-bin -y
RUN usermod -a -G video root

RUN \
  apt-get update && \
  apt-get install -y python3 python3-pip python3-dev omxplayer

RUN apt-get install -y libdbus-1-dev libdbus-glib-1-dev

ENV LANG="en_US.UTF-8"
ENV LC_ALL en_US.UTF-8
ENV TZ 'Europe/Moscow'

RUN pip3 install youtube_dl

ADD requirements.txt /app/
WORKDIR /app
RUN pip3 install -r requirements.txt

WORKDIR /app/code/
CMD rq worker youtube --url redis://redis:6379/0
