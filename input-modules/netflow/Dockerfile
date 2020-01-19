FROM python:3.7

RUN apt-get update && apt-get install nfdump -y

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY script.py .

CMD ["python", "-u", "script.py"]