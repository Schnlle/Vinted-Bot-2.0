# Dockerfile für deinen Vinted-Bot
FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "Bot.py"]
