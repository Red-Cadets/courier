FROM python:3.8.1-slim-buster

# установка переменных окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# установка системных зависимостей
RUN apt-get update && \
    pip install --upgrade pip

# установка зависимостей Python
COPY ./requirements.txt .
RUN pip install -r requirements.txt

ENV HOME=/home/app
ENV APP_HOME=/home/app/bot
RUN mkdir -p /home/app && groupadd app -g 901 && useradd app -g app -u 901 && mkdir $APP_HOME
WORKDIR $APP_HOME

# копирование всех файлов проекта в докер-контейнер
COPY . $APP_HOME

# изменение прав файлов на app:app
RUN chown -R 901:901 $APP_HOME
USER app

WORKDIR $APP_HOME/app

EXPOSE 5000
ENTRYPOINT ["/home/app/bot/entrypoint.sh"]