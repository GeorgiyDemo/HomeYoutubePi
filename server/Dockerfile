FROM raspbian/jessie

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install libraspberrypi-bin -y
RUN usermod -a -G video root

RUN \
  apt-get update && \
  apt-get install -y python3 python3-pip python3-dev omxplayer
ADD . /code
WORKDIR /code

ENV LANG="en_US.UTF-8"
ENV LC_ALL en_US.UTF-8
ENV TZ 'Europe/Moscow'

RUN pip3 install youtube_dl
RUN pip3 install -r requirements.txt
CMD omxplayer `youtube-dl -g -f best https://www.youtube.com/watch?v=uAWuyi9AnSo` -o local

