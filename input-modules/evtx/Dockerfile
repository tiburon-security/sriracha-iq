FROM python:3.7

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY script.py .
COPY evtxtoelk.py .
CMD ["python", "script.py"]