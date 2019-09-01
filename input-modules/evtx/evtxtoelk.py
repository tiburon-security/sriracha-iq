"""
MIT License

Copyright (c) 2018 Dan Gunter

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Minor changes made to original code to allow for username & password

"""

import contextlib
import mmap
import traceback
import json
from collections import OrderedDict
from datetime import datetime

from Evtx.Evtx import FileHeader
from Evtx.Views import evtx_file_xml_view
from elasticsearch import Elasticsearch, helpers
import xmltodict
import sys


class EvtxToElk:
    @staticmethod
    def bulk_to_elasticsearch(es, bulk_queue):
        try:
            helpers.bulk(es, bulk_queue)
            return True
        except:
            print(traceback.print_exc())
            return False

    @staticmethod
    def evtx_to_elk(filename, elk_ip, elk_user=None, elk_pass=None, elk_index="hostlogs", bulk_queue_len_threshold=500, metadata={}):
        bulk_queue = []
        if(elk_user==None or elk_pass==None):
            es = Elasticsearch([elk_ip], http_auth=(elk_user, elk_pass))
        else:
            es = Elasticsearch([elk_ip])
        with open(filename) as infile:
            with contextlib.closing(mmap.mmap(infile.fileno(), 0, access=mmap.ACCESS_READ)) as buf:
                fh = FileHeader(buf, 0x0)
                data = ""
                for xml, record in evtx_file_xml_view(fh):
                    try:
                        contains_event_data = False
                        log_line = xmltodict.parse(xml)

                        # Format the date field
                        date = log_line.get("Event").get("System").get("TimeCreated").get("@SystemTime")
                        if "." not in str(date):
                            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                        else:
                            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
                        log_line['@timestamp'] = str(date.isoformat())
                        log_line["Event"]["System"]["TimeCreated"]["@SystemTime"] = str(date.isoformat())

                        # Process the data field to be searchable
                        data = ""
                        if log_line.get("Event") is not None:
                            data = log_line.get("Event")
                            if log_line.get("Event").get("EventData") is not None:
                                data = log_line.get("Event").get("EventData")
                                if log_line.get("Event").get("EventData").get("Data") is not None:
                                    data = log_line.get("Event").get("EventData").get("Data")
                                    if isinstance(data, list):
                                        contains_event_data = True
                                        data_vals = {}
                                        for dataitem in data:
                                            try:
                                                if dataitem.get("@Name") is not None:
                                                    data_vals[str(dataitem.get("@Name"))] = str(
                                                        str(dataitem.get("#text")))
                                            except:
                                                pass
                                        log_line["Event"]["EventData"]["Data"] = data_vals
                                    else:
                                        if isinstance(data, OrderedDict):
                                            log_line["Event"]["EventData"]["RawData"] = json.dumps(data)
                                        else:
                                            log_line["Event"]["EventData"]["RawData"] = str(data)
                                        del log_line["Event"]["EventData"]["Data"]
                                else:
                                    if isinstance(data, OrderedDict):
                                        log_line["Event"]["RawData"] = json.dumps(data)
                                    else:
                                        log_line["Event"]["RawData"] = str(data)
                                    del log_line["Event"]["EventData"]
                            else:
                                if isinstance(data, OrderedDict):
                                    log_line = dict(data)
                                else:
                                    log_line["RawData"] = str(data)
                                    del log_line["Event"]
                        else:
                            pass

                        # Insert data into queue
                        #event_record = json.loads(json.dumps(log_line))
                        #event_record.update({
                        #    "_index": elk_index,
                        #    "_type": elk_index,
                        #    "metadata": metadata
                        #})
                        #bulk_queue.append(event_record)
                        event_data = json.loads(json.dumps(log_line))
                        event_data["_index"] = elk_index
                        event_data["_type"] = elk_index
                        event_data["meta"] = metadata
                        bulk_queue.append(event_data)

                        #bulk_queue.append({
                        #    "_index": elk_index,
                        #    "_type": elk_index,
                        #    "body": json.loads(json.dumps(log_line)),
                        #    "metadata": metadata
                        #})

                        if len(bulk_queue) == bulk_queue_len_threshold:
                            print('Bulkingrecords to ES: ' + str(len(bulk_queue)))
                            # start parallel bulking to ElasticSearch, default 500 chunks;
                            if EvtxToElk.bulk_to_elasticsearch(es, bulk_queue):
                                bulk_queue = []
                            else:
                                print('Failed to bulk data to Elasticsearch')
                                sys.exit(1)

                    except:
                        print("***********")
                        print("Parsing Exception")
                        print(traceback.print_exc())
                        print(json.dumps(log_line, indent=2))
                        print("***********")

                # Check for any remaining records in the bulk queue
                if len(bulk_queue) > 0:
                    print('Bulking final set of records to ES: ' + str(len(bulk_queue)))
                    if EvtxToElk.bulk_to_elasticsearch(es, bulk_queue):
                        bulk_queue = []
                    else:
                        print('Failed to bulk data to Elasticsearch')
                        sys.exit(1)