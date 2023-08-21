FROM python:3.9 as builder

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN rm requirements.txt

RUN apt-get update && apt-get install -y fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0 libatspi2.0-0 \
  libcairo2 libcups2 libdbus-1-3 libgbm1 libglib2.0-0 libgtk-3-0 libnspr4 libnss3 \
  libpango-1.0-0 libwayland-client0 libxcomposite1 libxkbcommon0 xdg-utils libu2f-udev libvulkan1

ARG CHROME_VERSION="114.0.5735.90-1"
RUN wget https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}_amd64.deb
RUN dpkg -i google-chrome-stable_${CHROME_VERSION}_amd64.deb
RUN rm -f google-chrome-stable_${CHROME_VERSION}_amd64.deb

RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

WORKDIR /app

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
