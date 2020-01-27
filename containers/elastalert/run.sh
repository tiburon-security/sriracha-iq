#!/bin/bash

# Setting login environment variables for login elasticsearch
export ES_USERNAME="$ELASTIC_USER"
export ES_PASSWORD="$ELASTIC_PASSWORD"

# Wait for start up before doing anything
until curl -u $ELASTIC_USER:$ELASTIC_PASSWORD -m 2 -Is http://elasticsearch:9200/ | grep "200 OK" > /dev/null; do
    sleep 5
	echo "Elasticsearch server not ready yet, retrying..."
done

elastalert-create-index --config /app/config.yml

python3 -m elastalert.elastalert --verbose --config /app/config.yml

echo "Starting elastalert"