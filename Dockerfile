# syntax=docker/dockerfile:1
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

# install app dependencies
RUN apt update 
RUN apt install -y python3 python3-pip
RUN apt install -y openjdk-8-jdk
RUN apt install -y openjdk-8-jre
RUN apt install -y firefox
RUN apt install -y firefox-geckodriver
RUN pip install selenium
RUN pip install BeautifulSoup4
RUN pip install lxml
RUN pip install webdriver-manager
RUN mkdir selen
RUN cd selen/

COPY Selenium.py /selen/

WORKDIR /selen/

ENTRYPOINT ["python3"]
CMD ["Selenium.py"]



