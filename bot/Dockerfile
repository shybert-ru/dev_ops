#Используем образ python 3.12
FROM python:3.12

WORKDIR /bot
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

#Запускаем бота
CMD ["python", "start.py"]
