FROM python:3.8.5-buster

ENV LANG="en_US.UTF-8"
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y locales
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen en_US.UTF-8 && \
    /usr/sbin/update-locale LANG=en_US.UTF-8
ENV LC_ALL en_US.UTF-8

ENV TZ 'Europe/Moscow'
RUN echo $TZ > /etc/timezone && \
  apt-get update && apt-get install -y tzdata && \
  rm /etc/localtime && \
  ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
  dpkg-reconfigure -f noninteractive tzdata && \
  apt-get clean

ADD requirements.txt /app/
WORKDIR /app

RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt

WORKDIR /app/code/
CMD ["python", "tlg.py"]