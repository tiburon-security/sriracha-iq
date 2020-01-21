![Architecture Diagram](https://raw.githubusercontent.com/tiburon-security/sriracha-iq/master/misc/SrirachaIQ_Architecture.png)

## Overview
This project is an instantiation of the Elastic Stack for the purposes of assessing system security and perofrming audits, a task commonly associated with independent blue teams, threat hunters, security control assessors, and cyber security auditors. It facilitates aggregation and analysis of commonly used log formats to include event logs (Windows & Linux) and vulnerability scanner logs, with more coming soon.

This tool was designed with the basic assumption that some central aggregation isn't already in place in the target environment & that the rules of engagement preclude installation of instrumentation (i.e. sysmon, filebeats, nxlog, rsyslog, nessus agents, etc...). As a result, the modus operandi requires manual extraction of logs & offline analysis, which is a difficult task that can be time consuming. This is a pretty common situation for independent assessors that aren't traditionally associated with the target environment being assessed. This project aims to aid in these types of scenarios by leveraging Elastic for centralization of this data, including ingestion processes for offline data and Kibana dashboards for visualizing & analyzing the data quickly to deliver quick assessments of the target environments.

Given this, the project is built in Docker, leveraging docker-compose, facilitating quick environments for building, data ingestion, analysis, and destruction. As a result, security features within Elastic are minimal as the service isn't intended to be public facing nor long running - it is intended to be run on either an analysis workstation or private server with limited access. Again, **do not** expose the Elastic components hosted on this system to neither the open internet nor a corporate/enterprise environment. 
## Data Inputs & their Common Location on target OS's:
As discussed in the Overview, the assumption is that we are working with data obtained manually & not via some centralized repository, for example manual extraction of evtx files for a Windows endpoint or manual download of the XML-based vulnerability scan report from nessus

## Viewing Data

### Kibana

To use Kibana, access port 80 which is exposed to the docker host. A variety of views, filters, dashboards, and visualizations are preconfigured and installed as part of the SrirachaIQ suite.

http://localhost:80

### Jupyter Lab Notebooks

For more advanced usage & custom analytics, Jupyter Notebooks have been integrated into the environment. The installation comes with basic elasticsearch libraries included & an example is included. The Jupyter Lab environment is exposed to the docker host over port 8888.

Notebooks:
 - jupyter/notebooks
 
 https://localhost:8888

## Data Inputs / Ingest

### Windows Data:

#### /data-inputs/evtx:
Windows XML Event Logs

	Windows Vista +, Server 2008 +:
	- C:\Windows\System32\winevt\Logs\[Application, Software, Security, etc.]

### Linux Data:

Note: On many falvors of Linux, if you just retrieve logs from the system directly, since the assumption is you can't just point rsyslog to you own collector, the year is ommited in the timestamps. This causes the ingest modules to just assume the current year, which in some cases could end up with events showing up in the future. For example, if the current date is Jan 18th 2020, and the log was retrieved December 1st 2019, the ingested events would show up as various dates in December 2020. If this is an issue for your analysis, there is a quick & dirty Python script for adding years to a log included in /misc/linux_logs_add_year.py; the script is compatible with Python 2.7+.

Sample Usage:

	cat /var/log/secure.log | python linux_logs_add_year.py 2019 > /tmp/auth_log_with_year.log

#### /data-inputs/syslog:
Generic system activity logs

	RHEL Based Linux:
	- /var/log/messages*

	Debian Based Linux:
	- /var/log/syslog*
	
#### /data-inputs/auth:
Authentication related event logs

	RHEL Based Linux:
	- /var/log/secure*

	Debian Based Linux:
	- /var/log/auth.log*
	
#### /data-inputs/auditd:
Audit daemon logs

	RHEL & Debian Based Linux:
	/var/log/audit/audit.log*
	
### Vulnerability Scan Data:

#### /data-inputs/nessus:
Nessus vulnerability scan data

	All versions:
	Export .nessus XML file from Security Center or Nessus

### Network Data:

#### /data-inputs/netflow:
Netflow records

	All nfcapd binary files supported by nfdump