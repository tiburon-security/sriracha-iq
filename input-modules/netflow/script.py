###
# Monitors input folder for Windows Event Log files (.evtx) & ships them to Elasticsearch 
###

import os
import time
from elasticsearch import Elasticsearch
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import PatternMatchingEventHandler

class Shipper(PatternMatchingEventHandler):
	"""
	Custom watchdog handler to ingest netflow into elasticsearch
	"""
	
	def __init__(self):
		super(Shipper, self).__init__(ignore_patterns=["*.csv", "*.keep"])
		
	def process(self, event):
		"""
		event.event_type 
			'modified' | 'created' | 'moved' | 'deleted'
		event.is_directory
			True | False
		event.src_path
			path/to/observed/file
		"""
		
		print(event.src_path)
		
		# parse ncapd file & generate csv, which is picked up by logstash
		os.system('nfdump -r {} -o csv -q > {}.csv'.format(event.src_path, event.src_path))
		
		# delete ncapd file
		try:
			os.remove(event.src_path)
		except:
			print("Error while deleting file {}".format(event.src_path))
		
	
	def on_created(self, event):
		self.process(event)


if __name__ == "__main__":
	"""
	Initiate watchdog
	"""
	
	print("Starting input module")

	path = "/data_inputs/netflow/"
	
	# Verify that elasticsearch is actually running first - 5 minute timeout
	es = Elasticsearch("http://elasticsearch:9200",  http_auth=(os.environ['ELASTIC_USER'],os.environ['ELASTIC_PASSWORD']), timeout=10, max_retries=30)
	print(es.info())

	event_handler = Shipper()
	observer = Observer()
	observer.schedule(event_handler, path, recursive=False)
	observer.start()
	
	try:
		while True:
			time.sleep(1)

	except KeyboardInterrupt:
		observer.stop()
		
	observer.join()