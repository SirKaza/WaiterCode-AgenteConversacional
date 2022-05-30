FROM python:3.10.4 AS BASE


WORKDIR /app

# upgrade pip version
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --upgrade setuptools
RUN pip3 install -U --user pip && pip3 install rasa
RUN pip install mysql-connector-python-rf
ADD config.yml config.yml
ADD domain.yml domain.yml
ADD credentials.yml credentials.yml
ADD endpoints.yml endpoints.yml