from elasticsearch import Elasticsearch, helpers
from ntc_templates.parse import parse_output
import traceback
import json

class Process:
    @staticmethod
    def bulk_to_elasticsearch(es, bulk_queue):
        try:
            helpers.bulk(es, bulk_queue)
            return True
        except:
            print(traceback.print_exc())
            return False

    @staticmethod
    def process(filename, elk_ip, elk_user=None, elk_pass=None, elk_index="hostlogs", platform="cisco_ios", bulk_queue_len_threshold=500):

        bulk_queue = []


        es = Elasticsearch([elk_ip], http_auth=(elk_user, elk_pass))

        with open(filename) as infile:
            rawData = infile.read()
            parsedData = parse_output(platform=platform, command="show", data=rawData)
            print(json.dumps(parsedData))
            pass
            '''
            event_data = json.loads(json.dumps(log_line))
            event_data["_index"] = elk_index
            event_data["_type"] = elk_index
            event_data["meta"] = metadata
            bulk_queue.append(event_data)


            if len(bulk_queue) == bulk_queue_len_threshold:
                print('Bulkingrecords to ES: ' + str(len(bulk_queue)))
                # start parallel bulking to ElasticSearch, default 500 chunks;
                if EvtxToElk.bulk_to_elasticsearch(es, bulk_queue):
                    bulk_queue = []
                else:
                    print('Failed to bulk data to Elasticsearch')
                    sys.exit(1)



            # Check for any remaining records in the bulk queue
            if len(bulk_queue) > 0:
                print('Bulking final set of records to ES: ' + str(len(bulk_queue)))
                if EvtxToElk.bulk_to_elasticsearch(es, bulk_queue):
                    bulk_queue = []
                else:
                    print('Failed to bulk data to Elasticsearch')
                    sys.exit(1)
            '''