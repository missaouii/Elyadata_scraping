FROM ubuntu:16.04
FROM python:3.8.13

USER root
# RUN commands
USER 1001

ADD Fastapi.py /usr/local/bin/
ADD Scraping.py /usr/local/bin/

USER root
RUN  apt-get update 
# RUN  apt-get install python3.9 -y
RUN  apt-get install python3-pip -y
RUN  apt-get install  unzip  -y
RUN  apt-get install  curl  -y
RUN  apt-get install  wget  -y
RUN  apt-get install -y libglib2.0-0 \
     libnss3 \
     libgconf-2-4 \
     libfontconfig1

RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

RUN pip3 install uvicorn
RUN pip3 install python-time
# RUN pip3 install os-sys
RUN pip3 install wget
RUN pip3 install selenium
RUN pip3 install Pillow
RUN pip3 install pydantic
RUN pip3 install pymongo
RUN pip3 install mongoengine
RUN pip3 install fastapi
RUN pip3 install pymongo[srv]

RUN cd /usr/local/bin/
EXPOSE 8000
CMD ["uvicorn", "Fastapi:app", "--host", "0.0.0.0"]