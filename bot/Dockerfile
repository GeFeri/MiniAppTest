FROM python:3.12-slim
WORKDIR /bot

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ✅ добавить сертификат в системное хранилище
COPY root.crt /usr/local/share/ca-certificates/root.crt
RUN apt-get update && apt-get install -y ca-certificates && update-ca-certificates

COPY . .
CMD ["python", "bot.py"]
