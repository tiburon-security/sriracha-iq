FROM python:3.6

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY config.yml .
COPY run.sh .

RUN chmod +x run.sh

ENTRYPOINT ["/app/run.sh"]