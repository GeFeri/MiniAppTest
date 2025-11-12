FROM python:3.12-slim
WORKDIR /bot

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .   # 👈 копируем весь код из ./bot внутрь /bot
CMD ["python", "bot.py"]
