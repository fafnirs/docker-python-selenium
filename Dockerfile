FROM joyzoursky/python-chromedriver:3.8-selenium

# - Vi・Vim が入っていないのでインストールする
# - pip をアップデートして pipienv をインストールする
RUN set -x && \
  apt-get update && \
  apt-get install -y vim && \
  pip install --upgrade pip && \
  pip install pipenv && \
  pip install browsermob-proxy && \
  pip install psutil && \
  pip install beautifulsoup4 && \
  pip install chromedriver-binary==79.0.3945.36.0