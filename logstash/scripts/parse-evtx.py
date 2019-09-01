####
# Simple script that prints XML structure for a Windows EVTX file to stdout
####

import sys
import Evtx.Evtx as evtx
import Evtx.Views as e_views


with evtx.Evtx(sys.argv[1]) as log:
	#print(e_views.XML_HEADER)
	#print("<Events>")
	
	#header = ("<Events>\n")
	sys.stdout.buffer.write("<Events>\n")
	sys.stdout.flush()
	
	for record in log.records():
		#print(record.xml())
		
		sys.stdout.buffer.write(record.xml() + "\n")
		sys.stdout.flush()
		
	#print("</Events>")
	
	#footer = ("</Events>\n").encode("cp1252")
	sys.stdout.buffer.write("</Events>\n")
	sys.stdout.flush()