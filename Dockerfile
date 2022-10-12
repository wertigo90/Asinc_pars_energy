# syntax=docker/dockerfile:1
FROM ubuntu:20.04

# install app dependencies
RUN apt update 
RUN apt install -y python3 python3-pip
RUN apt install -y openjdk-8-jdk
RUN apt install -y openjdk-8-jre
RUN apt install -y firefox
RUN pip install selenium
RUN pip install BeautifulSoup4
RUN pip install lxml
RUN pip install webdriver-manager

# install app
COPY Selenium.py /
COPY geckodriver /


# final configuration
ENV FLASK_APP=hello
EXPOSE 8000
CMD flask run --host 0.0.0.0 --port
