#Created By Zkikvidze

import requests
import json
import argparse


#Specify ASM Domain or IP
asmaddress = "CHANGEME"

#Specify username:password in base64
auth = "CHANGEME"


parser = argparse.ArgumentParser(description='BIG-IP ASM IP Address Blocker')

parser.add_argument('-a', '--address', help='IP Address', required=True)
parser.add_argument('-p', '--policy', help='Policy Full path. Example: /Common/website.ge_policy', required=True)
args = parser.parse_args()

asmauth = "Basic " + auth


def getPolicyId(fullPath):
	asmurl = "https://" + asmaddress + "/mgmt/tm/asm/policies?$select=id,fullPath"
	headers = {"Authorization": asmauth}
	r = requests.get(asmurl, verify=False, headers=headers)
	js = r.json()

	for item in js['items']:
		if item['fullPath'] == fullPath:
			return item['id']


def blockIp(ip, id):
	asmurl = "https://" + asmaddress + "/mgmt/tm/asm/policies/" + id + "/whitelist-ips"
	payload = {"blockRequests": "always", "description": "Blocked By API Client", "ipAddress": ip, "ipMask": "255.255.255.255", "neverLearnRequests": "true"}
	headers = {"Content-Type": "application/json", "Authorization": asmauth}
	requests.post(asmurl, verify=False, headers=headers, json=payload)


def applyPolicy(id):
	asmurl = "https://" + asmaddress + "/mgmt/tm/asm/tasks/apply-policy"
	policyurl = "https://localhost/mgmt/tm/asm/policies/" + id
	payload = { "policyReference": { "link" : policyurl } }
	headers = {"Content-Type": "application/json", "Authorization": asmauth}
	r = requests.post(asmurl, verify=False, headers=headers, json=payload)




blockIp(args.address, getPolicyId(args.policy))
applyPolicy(getPolicyId(args.policy))

