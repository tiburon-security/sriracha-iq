# Sriracha-IQ

## Overview
This project is an instantiation of the Elastic Stack for the purposes of assessing system security and perofrming audits, a task commonly associated with independent blue teams, threat hunters, security control assessors, and cyber security auditors. It facilitates aggregation and analysis of commonly used log formats to include event logs (Windows & Linux) and vulnerability scanner logs, with more coming soon.

This tool was designed with the basic assumption that some central aggregation isn't already in place in the target environment & that the rules of engagement preclude installation of instrumentation (i.e. sysmon, filebeats, nxlog, rsyslog, nessus agents, etc...). As a result, the modus operandi requires manual extraction of logs & offline analysis, which is a difficult task that can be time consuming. This is a pretty common situation for independent assessors that aren't traditionally associated with the target environment being assessed. This project aims to aid in these types of scenarios by leveraging Elastic for centralization of this data, including ingestion processes for offline data and Kibana dashboards for visualizing & analyzing the data quickly to deliver quick assessments of the target environments.

Given this, the project is built in Docker, leveraging docker-compose, facilitating quick environments for building, data ingestion, analysis, and destruction. As a result, security features within Elastic are minimal as the service isn't intended to be public facing nor long running - it is intended to be run on either an analysis workstation or private server with limited access. Again, **do not** expose the Elastic components hosted on this system to neither the open internet nor a corporate/enterprise environment. 
## Data Inputs & their Common Location on target OS's:
As discussed in the Overview, the assumption is that we are working with data obtained manually & not via some centralized repository, for example manual extraction of evtx files for a Windows endpoint or manual download of the XML-based vulnerability scan report from nessus

### Windows Data:

#### /data-inputs/evtx:
Windows XML Event Logs

	Windows Vista +, Server 2008 +:
	- C:\Windows\System32\winevt\Logs\[Application, Software, Security, etc.]

### Linux Data:

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
- Coming Soon