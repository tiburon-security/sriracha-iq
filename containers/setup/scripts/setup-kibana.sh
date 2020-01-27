#!/bin/bash

url=http://kibana:5601

echo "Kibana setup script starting."

# Wait for start up before doing anything
until curl -u $ELASTIC_USER:$ELASTIC_PASSWORD -m 2 -Is http://kibana:5601/app/kibana | grep "200 OK" > /dev/null; do
    sleep 5
	echo "Kibana server not ready yet, retrying..."
done

echo "Kibana server now available."

# Tests that the default settings haven't already been set before - this is to prevent the defaults from overwriting
# user changed upon restarts. Test whether one of the default indexes exists.
if ! curl -u $ELASTIC_USER:$ELASTIC_PASSWORD -s "$url/api/saved_objects/_find?type=index-pattern&search_fields=title&search=nessus" | grep --quiet "\"total\":1"; then 

    echo "Uploading kibana default saved objects"
  
    # Upload default saved objects for dashboards, indexes, and components  
    curl -u $ELASTIC_USER:$ELASTIC_PASSWORD -fsS -X POST $url/api/saved_objects/_import?overwrite=true -H "kbn-xsrf: true" --form file=@/app/extras/kibana-config.ndjson > /dev/null

else
    echo "Default kibana saved objects already uploaded, not reuploading"
	
fi

echo "Kibana setup script finished."