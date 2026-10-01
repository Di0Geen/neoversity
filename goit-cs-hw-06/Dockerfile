FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py index.html message.html error.html style.css logo.png ./

EXPOSE 3000

CMD ["python", "main.py"]