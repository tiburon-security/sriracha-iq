'''
On many falvors of Linux, if you just retrieve logs from the system directly, since the assumption is you can't just point rsyslog to you own collector, the year is ommited in the timestamps. This causes the ingest modules to just assume the current year, which in some cases could end up with events showing up in the future. For example, if the current date is Jan 18th 2020, and the log was retrieved December 1st 2019, the ingested events would show up as various dates in December 2020. If this is an issue for your analysis, this quick & dirty Python script adds years to a log; the script is compatible with Python 2.7+.

Sample Usage:

	cat /var/log/secure.log | python linux_logs_add_year.py 2019 > /tmp/auth_log_with_year.log
'''

import sys
import re
from datetime import datetime

timestamp = re.compile("([A-Za-z]{3})\s{1,2}([0-9]{1,2})\s{1}([0-9]{2}):([0-9]{2}):([0-9]{2})")

for line in sys.stdin.readlines():
	matched_timestamps = re.match(timestamp, line)
	
	date_object = datetime.strptime(matched_timestamps.group(0), "%b %d %X")
	date_object = date_object.replace(year=int(sys.argv[1]), tzinfo=None)
		
	sys.stdout.write(re.sub(timestamp,date_object.isoformat(),line))