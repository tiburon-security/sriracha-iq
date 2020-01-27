###
# Monitors the data input folders and ages files off when they reach 4 minutes old, with the assumption
# that the Beats have already processed them
###

import os
import time
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
import datetime
from dateutil.parser import parse
import json
import glob

class FileTracker(FileSystemEventHandler):
	"""
	Custom watchdog handler to watching 
	"""
		
	def __init__(self, DATA_INPUTS_FOLDER_PATH):
	
		# Maximum age of a file in seconds
		self.MAX_FILE_AGE = 240
	
		self.DATA_INPUTS_FOLDER_PATH = DATA_INPUTS_FOLDER_PATH
		self.DATABASE_FILE = "FILE_AGE.db"
		
		self.DATABASE_FILE_PATH = os.path.join(self.DATA_INPUTS_FOLDER_PATH, self.DATABASE_FILE)
		
		self.DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
		
		self.IGNORE_FILES = [".keep", 'README.md', self.DATABASE_FILE, "/data_inputs/sample-"]

		# Create DB file if it doesn't already exist
		with open(self.DATABASE_FILE_PATH, 'w'): pass
		
		
	def preprocess(self):
		"""
		Begins tracking files that already exist within the folder structure
		"""

		initial_file_ages = {}
				
		# All the files within the data input directories after filtering out known artifacts
		files = [file for file in glob.glob(os.path.join(self.DATA_INPUTS_FOLDER_PATH, "**"), recursive=True) if not any(ignore in file for ignore in self.IGNORE_FILES) and os.path.isfile(file)]
		
		for file in files:
			initial_file_ages[file] = datetime.datetime.utcnow().isoformat()

		with open(self.DATABASE_FILE_PATH, 'w') as f:
			print("Existing Files Detected:")
			print(json.dumps(initial_file_ages))
			f.write(json.dumps(initial_file_ages))				
	
	def process(self, event):
		"""
		Implements Watchdog lib's function for processing file changes
		
		event.event_type 
			'modified' | 'created' | 'moved' | 'deleted'
		event.is_directory
			True | False
		event.src_path
			path/to/observed/file
		"""
		
		if event.event_type == 'created' and not event.is_directory and not any(ignore in event.src_path for ignore in self.IGNORE_FILES):
		
			print("[ DETECTED ] {}".format(event.src_path))
			
			json_data = None
			
			with open(self.DATABASE_FILE_PATH, 'r') as f:
				json_data = json.load(f)
				
				# Track new file & current ISO timestamp
				json_data[event.src_path] = datetime.datetime.utcnow().isoformat()

			with open(self.DATABASE_FILE_PATH, 'w') as f:
				f.write(json.dumps(json_data))

		
	def delete_old_files(self):
		json_data = {}
		keys_to_delete = []
	
		# Find files that have exaceed age & delete from filesystem
		with open(self.DATABASE_FILE_PATH, 'r') as f:
			json_data = json.load(f)

			for path in json_data:
				original_detected_date = parse(json_data[path])
				timedelta = datetime.datetime.utcnow() - original_detected_date
				
				if(timedelta.total_seconds() >= self.MAX_FILE_AGE):
					print("[ EXPIRED ] {} ... deleting".format(path))
					os.remove(path)
					keys_to_delete.append(path)
		
		# Update file age tracking file
		for key in keys_to_delete: del json_data[key]

		with open(self.DATABASE_FILE_PATH, 'w') as f:
			f.write(json.dumps(json_data))		
		
		
	def on_created(self, event):
		self.process(event)


if __name__ == "__main__":
	"""
	Initiate watchdog
	"""
	
	print("[ STARTING ] Input Module Cleaner")

	DATA_INPUTS_FOLDER_PATH = "/data_inputs/"

	fileTracker = FileTracker(DATA_INPUTS_FOLDER_PATH)
	
	# Track any existing files
	fileTracker.preprocess()
	
	# Begin watching input folders
	observer = Observer()
	observer.schedule(fileTracker, DATA_INPUTS_FOLDER_PATH, recursive=True)
	observer.start()
	
	try:
		while True:
			time.sleep(30)
			
			# Delete files that have aged off
			fileTracker.delete_old_files()

	except KeyboardInterrupt:
		observer.stop()
		
	observer.join()