FROM python:3.12-slim

WORKDIR /bot

# Устанавливаем зависимости и сертификаты
RUN apt-get update && apt-get install -y ca-certificates && update-ca-certificates

# Копируем сертификат и обновляем хранилище
COPY root.crt /usr/local/share/ca-certificates/root.crt
RUN chmod 644 /usr/local/share/ca-certificates/root.crt && update-ca-certificates

# Устанавливаем Python-зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходники
COPY . .

CMD ["python", "bot.py"]
