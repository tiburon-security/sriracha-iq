#!/bin/bash

#set -euo pipefail

url=http://kibana:5601

echo "Kibana setup script starting."

# Wait for start up before doing anything
until curl -m 2 -Is http://kibana:5601/app/kibana | grep "200 OK" > /dev/null; do
    sleep 5
	echo "Kibana server not ready yet, retrying..."
done

echo "Kibana server now available."

curl -fsS -X POST $url/api/saved_objects/_import?overwrite=true -H "kbn-xsrf: true" --form file=@/app/extras/kibana-config.ndjson > /dev/null

echo "Kibana setup script finished."