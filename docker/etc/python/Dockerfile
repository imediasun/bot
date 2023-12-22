# Используйте официальный образ Python
FROM python:3.8

RUN apt-get update && apt-get install -y \
    python3-pip

# Установите рабочую директорию внутри контейнера
WORKDIR /var/www


# Копируйте файлы с зависимостями и код в контейнер
COPY ./api-backend/requirements.txt .

RUN pip install python-dotenv psycopg2-binary
RUN pip install setuptools
# Установите зависимости
RUN pip install -r requirements.txt

# Копируйте остальные файлы в контейнер
COPY ./api-backend .

# Укажите команду для запуска приложения
CMD ["python3", "startbot.py"]