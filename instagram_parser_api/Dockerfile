FROM python:3

ENV HOST_USERNAME=placeholder
ENV HOST_PASSWORD=placeholder

ENV PYTHON_PATH=instagram_parser_api
ENV FLASK_APP=api.py

WORKDIR /app

COPY src/ .
COPY requirements.txt .

RUN apt-get update
RUN apt-get install -y wget xvfb
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get -y install google-chrome-stable
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD flask run