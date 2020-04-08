###
# Monitors input folder for Windows Event Log files (.evtx) & ships them to Elasticsearch 
###

import os
import time
from elasticsearch import Elasticsearch
from process import Process
from elasticsearch import Elasticsearch
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

class Shipper(FileSystemEventHandler):
	"""
	Custom watchdog handler to ingest event logs into elasticsearch
	"""

	def __init__(self, platform):
		#super(self)
		self.platform = platform


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
		
		# parse evtx file & ship to elastic
		Process.process(event.src_path, "http://elasticsearch:9200", elk_user=os.environ['ELASTIC_USER'], elk_pass=os.environ['ELASTIC_PASSWORD'], elk_index="network-config-{}".format(os.environ['ELASTIC_VERSION']), platform=self.platform)
		
		# delete evtx file
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
	# Verify that elasticsearch is actually running first - 5 minute timeout
	es = Elasticsearch("http://elasticsearch:9200",  http_auth=(os.environ['ELASTIC_USER'],os.environ['ELASTIC_PASSWORD']), timeout=10, max_retries=30)
	print(es.info())


	'''

	'''
	print("Listening for Cisco iOS Configurations")
	ciscoIosPath = "/data_inputs/network-configs/cisco-ios/"
	ciscoIosHandler = Shipper(platform="cisco_ios")
	ciscoIosObserver = Observer()
	ciscoIosObserver.schedule(ciscoIosHandler, ciscoIosPath, recursive=False)
	ciscoIosObserver.start()

	print("Listening for Cisco NXOS Configurations")
	ciscoNxosPath = "/data_inputs/network-configs/cisco-nxos"
	ciscoNxosHandler = Shipper(platform="cisco_nxos")
	ciscoNxosObserver = Observer()
	ciscoNxosObserver.schedule(ciscoNxosHandler, ciscoNxosPath, recursive=False)
	ciscoNxosObserver.start()

	try:
		while True:
			time.sleep(1)

	except KeyboardInterrupt:
		ciscoIosObserver.stop()
		ciscoNxosObserver.stop()

	ciscoIosObserver.join()
	ciscoNxosObserver.join()