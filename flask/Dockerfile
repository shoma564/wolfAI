FROM ubuntu:18.04

RUN apt -y update
RUN apt -y install python3 python3-pip curl wget
RUN apt autoremove
RUN pip3 install --upgrade pip setuptools


RUN mkdir -p /usr/src/app/templates
ADD ./requirements.txt /usr/src/app/
ADD ./app.py /usr/src/app/
ADD ./templates /usr/src/app/templates
RUN pip3 install --no-cache-dir -r /usr/src/app/requirements.txt


WORKDIR /usr/src/app/
CMD ["python3", "/usr/src/app/app.py"]
