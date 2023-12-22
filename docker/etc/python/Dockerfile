# Используйте официальный образ Python
FROM python:3.8

# Установите рабочую директорию внутри контейнера
WORKDIR /var/www

# Копируйте файлы с зависимостями и код в контейнер
COPY ./api-backend/requirements.txt .

# Установите зависимости
RUN pip install -r requirements.txt

# Копируйте остальные файлы в контейнер
COPY ./api-backend .

# Укажите команду для запуска приложения
CMD ["python", "main.py"]